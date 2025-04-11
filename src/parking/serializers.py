from rest_framework import serializers
from .models import (
    Parking, ParkingPhoto, ParkingReview,
    ParkingReservation
)
from accounts.serializers import UserSerializer


class ParkingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingPhoto
        fields = '__all__'


class ParkingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingReview
        fields = '__all__'


class ParkingSerializer(serializers.ModelSerializer):
    photos = ParkingPhotoSerializer(many=True, read_only=True)
    reviews = ParkingReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Parking
        fields = '__all__'


class ParkingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


class ParkingReservationSerializer(serializers.ModelSerializer):
    parking = ParkingSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ParkingReservation
        fields = '__all__'
