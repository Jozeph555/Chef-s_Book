from src.modules.ui.main_loop import MainLoop
from src.modules.models.booking_model import Booking
from src.modules.models.customer_model import Customer
from src.modules.service.bookings_service import BookingsService
from src.modules.service.customers_service import CustomerService


def main():
    # Example
    customer_service = CustomerService()
    booking_service = BookingsService()

    customer1 = Customer()
    customer1.name = "Test"
    customer1.birthday = "01.01.2000"

    customer2 = Customer()
    customer2.name = "Test2"

    booking1 = Booking()
    booking1.customer_id = customer1.id
    booking1.date = "01.01.2022 00:00"

    customer_service.extend([customer1, customer2])
    booking_service.extend([booking1])

    customer_service.save()
    booking_service.save()

    main_loop = MainLoop()
    main_loop.run()


if __name__ == "__main__":
    main()
