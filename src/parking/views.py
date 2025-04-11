from rest_framework import viewsets
from .models import ParkingReservation
from .serializers import (
    ParkingSerializer, ParkingCreateUpdateSerializer,
    ParkingReservationSerializer
)
from .repository import (
    ParkingRepository, ParkingPhotoRepository,
    ParkingReviewRepository, ParkingReservationRepository
)


class ParkingViewSet(viewsets.ModelViewSet):
    queryset = ParkingRepository.get_all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ParkingSerializer
        elif self.action == ['create', 'update', 'destroy']:
            return ParkingCreateUpdateSerializer


class ParkingReservationViewSet(viewsets.ModelViewSet):
    lookup_field = 'phone'

    def get_queryset(self):
        return ParkingReservationRepository.get_by_phone(phone=self.kwargs['phone'])

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ParkingReservationSerializer
