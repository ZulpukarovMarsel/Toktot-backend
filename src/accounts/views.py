from django.db import IntegrityError
from rest_framework import generics, status, response, exceptions, viewsets
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    SignUpSerializer, SignInSerializer, UserSerializer,
    SendOTPSerializer, VerifyOTPSerializer, SetCarPlateSerializer
)
from .services import (
    GetLoginResponseService, SmsService, CarPlateService,
)
from .repository import AccountRepository, OTPRepository


class SignUpAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = User.objects.create_user(
                                                    phone=serializer.validated_data["phone"],
                                                    username=serializer.validated_data["username"],
                                                    car_plate=serializer.validated_data["car_plate"]
                                                )
                return response.Response(
                    data=GetLoginResponseService.get_login_response(user, request)
                )

            else:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return response.Response(
                data={
                    "detail": "Пользователь с данной номером существует!",
                    "status": status.HTTP_409_CONFLICT
                }
            )


class SignInAPIView(generics.CreateAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if not user:
            raise exceptions.AuthenticationFailed

        return response.Response(
            data=GetLoginResponseService.get_login_response(user, request)
        )


class OTPAPIView(generics.CreateAPIView):
    serializer_class = SendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp_code = SmsService.generate_otp()
        data = {
            "phone": phone,
            "otp": otp_code
        }
        message = f"Ваш код никому не показывайте {otp_code}"
        SmsService.send_sms(phone, message)
        OTPRepository.create(data)

        return response.Response(
            data={
                "message": "OTP sent successfully",
                "status": status.HTTP_201_CREATED
            }
        )


class VerifyOTPView(generics.CreateAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        otp_code = serializer.validated_data["otp"]

        otp_instance = OTPRepository.get_by_phone(phone, otp_code)
        if otp_instance:
            otp_instance.delete()
            return response.Response(
                data={
                    "message": "OTP verified successfully",
                    "status": status.HTTP_200_OK
                }
            )
        else:
            return response.Response(
                data={
                    "message": "Invalid OTP",
                    "status": status.HTTP_400_BAD_REQUEST
                }
            )


class SetCarPlateView(generics.CreateAPIView):
    serializer_class = SetCarPlateSerializer

    def post(self, request, *args, **kwargs):
        car_plate = request.FILES.get("car_plate_photo")

        if not car_plate:
            return response.Response(
                data={"message": "No car plate image provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            plate = CarPlateService.extract_license_plate(car_plate)
            return response.Response(
                data={"plate": plate},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return response.Response(
                data={"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProfilVIewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_queryset(self):
        if self.action in ["retrieve",  "update"]:
            return AccountRepository.get_by_username(self.kwargs["username"])

    def get_serializer_class(self):
        if self.action in ["retrieve", "update"]:
            return UserSerializer
        return super().get_serializer_class()
