from config.repository import BaseRepository
from .models import Parking, ParkingPhoto, ParkingReview, ParkingReservation


class ParkingRepository(BaseRepository):
    """
    Репозиторий для работы с моделью Parking.
    """
    model = Parking

    @classmethod
    def get_by_user(cls, user):
        """
        Возвращает парковку по пользователю.
        """
        return cls.model.objects.filter(user=user).first()


class ParkingPhotoRepository(BaseRepository):
    """
    Репозиторий для работы с моделью ParkingPhoto.
    """
    model = ParkingPhoto


class ParkingReviewRepository(BaseRepository):
    """
    Репозиторий для работы с моделью ParkingReview.
    """
    model = ParkingReview


class ParkingReservationRepository(BaseRepository):
    """
    Репозиторий для работы с моделью ParkingReservation.
    """
    model = ParkingReservation

    @classmethod
    def get_by_phone(cls, phone):
        """
        Возвращает парковку по номеру телефона.
        """
        return cls.model.objects.filter(user__phone=phone)
