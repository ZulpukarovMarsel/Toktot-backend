from django.urls import path
from .views import (
    SignUpAPIView, SignInAPIView, OTPAPIView,
    VerifyOTPView, SetCarPlateView
)

urlpatterns = [
    path('sign_up/', SignUpAPIView.as_view(), name='sign_up'),
    path('sign_in/', SignInAPIView.as_view(), name='sign_in'),
    path('otp/', OTPAPIView.as_view(), name='otp'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('set_car_plate/', SetCarPlateView.as_view(), name='set_car_plate')
]
