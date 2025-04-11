from rest_framework import serializers
from .models import User, OTP
from .services import SmsService


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("phone", "username", "car_plate")


class SignInSerializer(serializers.Serializer):
    phone = serializers.CharField()


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=4)


class SetCarPlateSerializer(serializers.Serializer):
    car_plate_photo = serializers.ImageField()
