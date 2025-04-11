from django.db import models


class Parking(models.Model):
    """
    Модель парковки.
    """
    name = models.CharField(max_length=255, verbose_name='Название')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    price_per_hour = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена за час'
    )
    total_spaces = models.PositiveIntegerField(verbose_name='Всего мест')
    available_spaces = models.PositiveIntegerField(verbose_name='Доступно мест')

    def __str__(self) -> str:
        return self.name or "No name"


class ParkingPhoto(models.Model):
    """
    Модель фотографии парковки.
    """
    parking = models.ForeignKey(
        Parking, on_delete=models.CASCADE, related_name='photos', verbose_name='Парковка'
    )
    photo = models.ImageField(upload_to='parking/photos/', verbose_name='Фото')

    def __str__(self) -> str:
        return f"Photo of {self.parking}"


class ParkingReview(models.Model):
    """
    Модель отзыва о парковке.
    """
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    parking = models.ForeignKey(
        Parking, on_delete=models.CASCADE, related_name='reviews', verbose_name='Парковка'
    )
    rating = models.PositiveIntegerField(verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self) -> str:
        return f"{self.user} - {self.parking} ({self.rating})"


class ParkingReservation(models.Model):
    """
    Модель бронирования парковки.
    """
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    parking = models.ForeignKey(
        Parking, on_delete=models.CASCADE, verbose_name='Парковка'
    )
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')

    def __str__(self) -> str:
        return f"{self.user} - {self.parking} ({self.start_time} - {self.end_time})"
