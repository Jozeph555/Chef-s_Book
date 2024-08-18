from datetime import datetime
from typing import List

from src.modules.dto.customer_dto import CustomerDTO
from src.modules.models.customer_model import Customer
from src.modules.service.base_service import BaseService

FILENAME = ".customers.csv"


class CustomerService(BaseService[CustomerDTO, Customer]):
    """Storing and managing customers"""

    def __init__(self):
        super().__init__(CustomerDTO, Customer, FILENAME)

    def customer_birthdays(self, date_range: int = 7) -> List[Customer]:
        today = datetime.today().date()
        upcoming_birthdays: List[Customer] = []

        for record in self:
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()
            upcoming_birthday = birthday.replace(year=today.year)

            # birthday has passed this year
            if today > upcoming_birthday:
                upcoming_birthday = birthday.replace(year=today.year + 1)

            days_delta = (upcoming_birthday - today).days

            # birthday is not in the next x days
            if 0 > days_delta or days_delta > date_range:
                continue

            upcoming_birthdays.append(record)

        return upcoming_birthdays

    def find_by_name(self, name: str) -> List[Customer]:
        return [customer for customer in self if customer.name.value == name]

    def find_by_phone(self, phone: str) -> List[Customer]:
        return [customer for customer in self if customer.has_phone(phone)]

    def find_by_email(self, email: str) -> List[Customer]:
        return [customer for customer in self if customer.email.value == email]

    def find_by_birthday(self, birthday: str) -> List[Customer]:
        return [customer for customer in self if customer.birthday.value == birthday]

    def find_by_note(self, note: str) -> List[Customer]:
        return [customer for customer in self if customer.has_note(note)]

    def find_by_tag(self, tag: str) -> List[Customer]:
        return [customer for customer in self if any(tag in note.tags for note in customer.notes)]

    def sort_by_tags(self) -> List[Customer]:
        return sorted(self, key=lambda customer: sorted([tag for note in customer.notes for tag in note.tags]))
