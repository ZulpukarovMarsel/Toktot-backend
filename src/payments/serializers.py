from rest_framework import serializers
from .models import PayPalCard


class AddPayPalCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=19)
    expiry_month = serializers.CharField(max_length=2)
    expiry_year = serializers.CharField(max_length=4)
    cvv = serializers.CharField(max_length=4)
    save_card = serializers.BooleanField(default=True)


class PayPalCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPalCard
        fields = ['id', 'last4', 'brand', 'is_default', 'created_at']


class ChargeWithSavedCardSerializer(serializers.Serializer):
    card_id = serializers.IntegerField()
    cvv = serializers.CharField(max_length=4)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
