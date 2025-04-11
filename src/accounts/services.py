import random
import easyocr
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client
from decouple import config
from ultralytics import YOLO
from django.conf import settings
import os
import requests


TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')


class GetLoginResponseService:
    @staticmethod
    def get_login_response(user, request):
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return data


class SmsService:

    @staticmethod
    def generate_otp():
        return random.randint(1000, 9999)

    @staticmethod
    def send_sms(phone, message):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        try:
            message = client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=phone
            )
            print(f"SMS-{phone} | SID-{message.sid}")
        except Exception as e:
            print(f"Error sending SMS: {e}")


class CarPlateService:
    model_path = os.path.join(
        settings.BASE_DIR, 'config', 'runs',
        'detect', 'train12', 'weights',
        'best.pt'
    )
    model = YOLO(model_path)
    reader = easyocr.Reader(['en', 'ru'], gpu=False)

    @staticmethod
    def extract_license_plate(photo):
        API_TOKEN_PLATE = config('API_TOKEN_PLATE')

        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files={'upload': photo},
            headers={'Authorization': f'Token {API_TOKEN_PLATE}'}
        )

        data = response.json()

        for result in data.get("results", []):
            return {
                "plate": result["plate"].upper(),
                # "score": result["score"],
                # "region": result.get("region", {}).get("code", "неизвестно")
            }

        return {"message": "Номер не найден"}

    # @staticmethod
    # def parser_car_plate(path):
