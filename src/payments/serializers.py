from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'last4', 'brand', 'added_at']


class TopUpSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    card_id = serializers.IntegerField()
    cvv = serializers.CharField(max_length=4)


class AddCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=19)
    expiry_month = serializers.CharField(max_length=2)
    expiry_year = serializers.CharField(max_length=2)
    cvv = serializers.CharField(max_length=4)
