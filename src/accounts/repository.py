from config.repository import BaseRepository
from .models import User, OTP


class AccountRepository(BaseRepository):
    """
    Репозиторий для работы с моделью User.
    """
    model = User

    @classmethod
    def get_by_username(cls, username: str) -> User:
        """
        Возвращает объект User по username.
        """
        return cls.model.objects.filter(username=username).first()

    @classmethod
    def get_by_car_plate(cls, car_plate: str) -> User:
        """
        Возвращает объект User по номеру машины.
        """
        return cls.model.objects.filter(car_plate=car_plate).first()


class OTPRepository(BaseRepository):
    """
    Репозиторий для работы с моделью OTP.
    """
    model = OTP

    @classmethod
    def get_by_phone(cls, phone: str, otp: int) -> OTP:
        """
        Возвращает объект OTP по номеру телефона.
        """
        return cls.model.objects.filter(phone=phone, otp=otp).first()
