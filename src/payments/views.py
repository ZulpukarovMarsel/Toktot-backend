import paypalrestsdk
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from .serializers import (
    AddPayPalCardSerializer, PayPalCardSerializer, ChargeWithSavedCardSerializer
)
from .models import PayPalCard


class ChargeWithSavedCardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChargeWithSavedCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            card = PayPalCard.objects.get(
                id=serializer.validated_data['card_id'], user=request.user
            )
        except PayPalCard.DoesNotExist:
            return Response({"error": "Card not found"}, status=404)

        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card_token": {
                        "credit_card_id": card.payment_token,
                        "cvv2": serializer.validated_data['cvv']
                    }
                }]
            },
            "transactions": [{
                "amount": {
                    "total": str(serializer.validated_data['amount']),
                    "currency": "USD"
                },
                "description": "Balance top-up"
            }]
        })

        if payment.create() and payment.execute():
            request.user.balance += Decimal(serializer.validated_data['amount'])
            request.user.save()
            return Response({"status": "success", "new_balance": request.user.balance})
        else:
            return Response({"error": payment.error}, status=400)


class PayPalCardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards = PayPalCard.objects.filter(user=request.user)
        serializer = PayPalCardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddPayPalCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })

        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "credit_card",
                    "funding_instruments": [{
                        "credit_card": {
                            "number": serializer.validated_data['card_number'],
                            "type": self._detect_card_type(serializer.validated_data['card_number']),
                            "expire_month": serializer.validated_data['expiry_month'],
                            "expire_year": serializer.validated_data['expiry_year'],
                            "cvv2": serializer.validated_data['cvv']
                        }
                    }]
                },
                "transactions": [{
                    "amount": {
                        "total": "1.00",
                        "currency": "USD"
                    },
                    "payee": {
                        "email": "sb-zvumz39761705@business.example.com"
                    },
                    "description": "Card verification"
                }]
            })

            if payment.create():
                funding_instr = payment.payer.funding_instruments[0].credit_card
                card = PayPalCard.objects.create(
                    user=request.user,
                    payment_token=funding_instr.credit_card_token.credit_card_id,
                    last4=funding_instr.number[-4:],
                    brand=funding_instr.type.lower(),
                    expiry_month=funding_instr.expire_month,
                    expiry_year=funding_instr.expire_year
                )

                if not PayPalCard.objects.filter(user=request.user, is_default=True).exists():
                    card.is_default = True
                    card.save()

                return Response(PayPalCardSerializer(card).data, status=201)
            else:
                return Response({"error": payment.error}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def _detect_card_type(self, card_number: str) -> str:
        """Определяет тип карты по её номеру"""
        if card_number.startswith('4'):
            return 'visa'
        if card_number[:2].isdigit() and 51 <= int(card_number[:2]) <= 55:
            return 'mastercard'
        if card_number.startswith('34') or card_number.startswith('37'):
            return 'amex'
        if card_number.startswith('6'):
            return 'discover'
        return 'visa'
