from src.modules.dto.booking_dto import BookingDTO
from src.modules.models.booking_model import Booking
from src.modules.service.base_service import BaseService

FILENAME = ".bookings.csv"


class BookingsService(BaseService[BookingDTO, Booking]):
    """Storing and managing customers"""

    def __init__(self):
        super().__init__(BookingDTO, Booking, FILENAME)
