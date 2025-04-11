from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
import requests
import uuid

from .models import Card
from .serializers import TopUpSerializer, AddCardSerializer, CardSerializer


class CardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cards = Card.objects.filter(user=user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        data = serializer.validated_data

        payload = {
            "card_number": data['card_number'],
            "expiry_month": data['expiry_month'],
            "expiry_year": data['expiry_year'],
            "cvv": data['cvv'],
            "user_id": str(user.id),
        }

        response = requests.post("https://api.optimapay.kg/add_card", json=payload)
        if response.status_code == 200:
            res = response.json()
            if res.get("success"):
                card_token = res["card_token"]
                last4 = res.get("last4", data['card_number'][-4:])
                brand = res.get("brand", "unknown")

                Card.objects.create(
                    user=user,
                    token=card_token,
                    last4=last4,
                    brand=brand
                )

                return Response({"status": "success", "message": "Карта добавлена"})
            else:
                return Response({"status": "fail", "message": res.get("error_message")})
        return Response({"status": "error", "details": response.text}, status=500)


class TopUpBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TopUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        card_id = serializer.validated_data['card_id']
        cvv = serializer.validated_data['cvv']
        user = request.user

        try:
            card = Card.objects.get(id=card_id, user=user)
        except Card.DoesNotExist:
            return Response({"error": "Карта не найдена"}, status=404)

        payload = {
            "amount": float(amount),
            "currency": "KGS",
            "card_token": card.token,
            "cvv": cvv,
            "order_id": f"{user.id}_topup_{uuid.uuid4()}",
            "description": "Пополнение баланса парковки"
        }

        response = requests.post("https://api.optimapay.kg/topup", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                user.balance += Decimal(amount)
                user.save()
                return Response({"status": "success", "message": "Баланс пополнен"})
            else:
                return Response({"status": "fail", "message": data.get("error_message")})
        return Response({"status": "error", "details": response.text}, status=500)
