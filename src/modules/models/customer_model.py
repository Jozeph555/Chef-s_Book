from typing import List, Optional

from src.modules.dto.customer_dto import CustomerDTO
from src.modules.models.fields.address_field import AddressField
from src.modules.models.fields.date_field import DateField
from src.modules.models.fields.email_field import EmailField
from src.modules.models.fields.id_field import IDField
from src.modules.models.fields.name_field import NameField
from src.modules.models.fields.phone_field import PhoneField


class Customer:
    """Class for storing customer info"""

    def __init__(self, dto: CustomerDTO = None):
        if not dto:
            dto = CustomerDTO()

        self._id = IDField(dto.id)
        self._name = NameField(dto.name, validate=False)
        self._birthday = DateField(dto.birthday, validate=False)
        self._address = AddressField(dto.address, validate=False)
        self._email = EmailField(dto.email, validate=False)
        self._phones = [PhoneField(phone, validate=False) for phone in dto.phones]

    @property
    def id(self) -> str:
        return str(self._id)

    @property
    def name(self) -> str:
        return self._name.value

    @name.setter
    def name(self, name: str) -> None:
        self._name = NameField(name)

    @property
    def phones(self) -> List[str]:
        return [phone.value for phone in self._phones]

    @phones.setter
    def phones(self, phones: List[str]) -> None:
        self._phones = [PhoneField(phone) for phone in phones]

    @property
    def birthday(self) -> Optional[str]:
        return str(self._birthday) if self._birthday.value else None

    @birthday.setter
    def birthday(self, birthday: str) -> None:
        self._birthday = DateField(birthday)

    @property
    def address(self) -> Optional[str]:
        return self._address.value if self._address else None

    @address.setter
    def address(self, address: str) -> None:
        self._address = AddressField(address)

    @property
    def email(self) -> Optional[str]:
        return self._email.value if self._email else None

    @email.setter
    def email(self, email: str) -> None:
        self._email = EmailField(email)

    def add_phone(self, phone_number: str) -> None:
        self._phones.append(PhoneField(phone_number))

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        self.remove_phone(old_phone_number)
        self.add_phone(new_phone_number)

    def remove_phone(self, phone_number: str) -> None:
        for index, p in enumerate(self._phones):
            if p.value == phone_number:
                del self._phones[index]
                return

    def has_phone(self, phone_number: str) -> bool:
        for phone in self._phones:
            if phone.value == phone_number:
                return True
        return False

    def dto(self) -> CustomerDTO:
        return CustomerDTO(
            id=str(self.id),
            name=str(self.name),
            phones=[str(phone) for phone in self._phones],
            birthday=str(self.birthday),
            address=str(self.address),
            email=str(self.email),
        )

    def __str__(self) -> str:
        return f"Customer name: {self.name}, phones: {'; '.join(self.phones)}"
