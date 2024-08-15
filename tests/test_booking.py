import unittest

from src.modules.dto.booking_dto import BookingDTO
from src.modules.models.booking_model import Booking


class TestBooking(unittest.TestCase):
    def setUp(self) -> None:
        dto = BookingDTO(id="1", customer_id="test_customer", date="01.01.2024 00:00")
        self.booking = Booking(dto)

    def test_initialization(self):
        self.assertEqual(self.booking.id, "1")
        self.assertEqual(self.booking.customer_id, "test_customer")
        self.assertEqual(self.booking.date, "01.01.2024 00:00")

    def test_empty_initialization(self):
        booking = Booking()
        self.assertIsNotNone(booking.id)
        self.assertIsNone(booking.customer_id)
        self.assertIsNone(booking.date)

    # def test_date_setter(self):
    #     new_date = "01.01.2024 10:00"
    #     self.booking.date = new_date
    #     self.assertEqual(self.booking.date, new_date)

    def test_dto_conversion(self):
        dto = self.booking.dto()
        self.assertEqual(dto.id, "1")
        self.assertEqual(dto.customer_id, "test_customer")
        self.assertEqual(dto.date, "01.01.2024 00:00")


if __name__ == '__main__':
    unittest.main()
