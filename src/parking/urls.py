from .views import (
    ParkingViewSet, ParkingReservationViewSet
)
from django.urls import path

urlpatterns = [
    path(
        'parking/',
        ParkingViewSet.as_view(
            {'get': 'list', 'post': 'create'}
        ),
        name='parking-list'
    ),
    path(
        'parking/<int:pk>/',
        ParkingViewSet.as_view(
            {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
        ),
        name='parking-detail'
    ),
    path(
        'reservation/',
        ParkingReservationViewSet.as_view(
            {'get': 'list', 'post': 'create'}
        ),
        name='reservation-list'
    ),
    path(
        'reservation/<int:pk>/',
        ParkingReservationViewSet.as_view(
            {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
        ),
        name='reservation-detail'
    ),
]
