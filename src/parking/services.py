from .models import Parking, ParkingReservation


class ParkingReservationService:
    """
    Сервис для работы с парковками и бронированиями.
    """

    def __init__(self, parking: Parking):
        self.parking = parking

    def reserve_parking(self, user, start_time, end_time):
        """
        Метод для бронирования парковки.
        """
        if self.parking.available_spaces > 0:
            reservation = ParkingReservation(
                user=user,
                parking=self.parking,
                start_time=start_time,
            )
            reservation.save()
            self.parking.available_spaces -= 1
            self.parking.save()
            return reservation
        else:
            raise ValueError("No available spaces")