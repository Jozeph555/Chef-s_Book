from typing import List

from src.modules.dto.booking_dto import BookingDTO
from src.modules.models.booking_model import Booking
from src.modules.service.base_service import BaseService

FILENAME = ".bookings.csv"


class BookingsService(BaseService[BookingDTO, Booking]):
    """Storing and managing customers"""

    def __init__(self):
        super().__init__(BookingDTO, Booking, FILENAME)

    def find_by_customer_id(self, customer_id: str) -> List[Booking]:
        """Find bookings by customer id"""
        return [booking for booking in self if booking.customer_id == customer_id]

    def find_by_date(self, date: str) -> List[Booking]:
        """Find bookings by date"""
        return [booking for booking in self if booking.date == date]
