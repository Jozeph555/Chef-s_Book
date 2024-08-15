import re
from datetime import datetime
from typing import List, Optional


class Field():
    """Base field class"""

    def __init__(self, value):
        self._validate(value)
        self.value = self._parse(value)

    def __str__(self):
        return str(self.value)

    def _validate(self, value):
        """Method to validate the input value"""
        pass

    def _parse(self, value):
        """Method to parse the input value (if needed)"""
        return value


class Name(Field):
    MIN_LENGTH = 3
    MAX_LENGTH = 40

    def __init__(self, value):
        super().__init__(value)

    def _validate(self, value):
        if not Name.MIN_LENGTH <= len(value) <= Name.MAX_LENGTH:
            raise ValueError(f"The name '{value}' was not added. "
                             f"The name must be between {Name.MIN_LENGTH} and {Name.MAX_LENGTH} characters long.")


class Phone(Field):
    LENGTH = 10

    def __init__(self, value):
        super().__init__(value)

    def _validate(self, value):
        if not value.isdigit():
            raise ValueError(f"The phone number '{value}' was not added. "
                             f"The phone number must contain only digits.")
        if len(value) != Phone.LENGTH:
            raise ValueError(f"The phone number '{value}' was not added. "
                             f"The phone number must contain {Phone.LENGTH} digits.")


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return self.value.strftime(Birthday.DATE_FORMAT)

    def _validate(self, value):
        try:
            self._parse(value)
        except ValueError:
            raise ValueError(f"Invalid date format. Use {Birthday.DATE_FORMAT}")

    def _parse(self, value):
        return datetime.strptime(value, Birthday.DATE_FORMAT).date()


class Address(Field):
    MIN_LENGTH = 3
    MAX_LENGTH = 255

    def __init__(self, value):
        super().__init__(value)

    def _validate(self, value):
        if not Address.MIN_LENGTH <= len(value) <= Address.MAX_LENGTH:
            raise ValueError(
                f"The address '{value}' was not added. "
                f"The address must be between {Address.MIN_LENGTH} and {Address.MAX_LENGTH} characters long.")

        components = value.split(',')
        if not len(components) >= 2 and all(component.strip() for component in components):
            raise ValueError(
                f"The address '{value}' was not added. "
                f"Format of the address should be: '[Address Line 1], [City], [Country]'.")


class Email(Field):
    EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")

    def __init__(self, value):
        super().__init__(value)

    def _validate(self, value):
        if not Email.EMAIL_PATTERN.match(value):
            raise ValueError(f"The email '{value}' was not added. The email must be in a valid format.")


class ContactRecord:
    """Class for storing contact info"""

    def __init__(self, name: str):
        self._name = Name(name)
        self._phones: List[Phone] = []
        self._birthday: Optional[Birthday] = None
        self._address: Optional[Address] = None
        self._email: Optional[Email] = None

    @property
    def name(self) -> str:
        return self._name.value

    @name.setter
    def name(self, name: str) -> None:
        self._name = Name(name)

    @property
    def phones(self) -> List[str]:
        return [phone.value for phone in self._phones]

    @phones.setter
    def phones(self, phones: List[str]) -> None:
        self._phones = [Phone(phone) for phone in phones]

    @property
    def birthday(self) -> Optional[str]:
        return str(self._birthday) if self._birthday else None

    @birthday.setter
    def birthday(self, birthday: str) -> None:
        self._birthday = Birthday(birthday)

    @property
    def address(self) -> Optional[str]:
        return self._address.value if self._address else None

    @address.setter
    def address(self, address: str) -> None:
        self._address = Address(address)

    @property
    def email(self) -> Optional[str]:
        return self._email.value if self._email else None

    @email.setter
    def email(self, email: str) -> None:
        self._email = Email(email)

    def add_phone(self, phone_number: str) -> None:
        self._phones.append(Phone(phone_number))

    def find_phone(self, phone_number: str) -> Optional[str]:
        for phone in self._phones:
            if phone.value == phone_number:
                return phone.value
        return None

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        self.remove_phone(old_phone_number)
        self.add_phone(new_phone_number)

    def remove_phone(self, phone_number: str) -> None:
        for index, p in enumerate(self._phones):
            if p.value == phone_number:
                del self._phones[index]
                return

    def __str__(self) -> str:
        return f"Contact name: {self.name}, phones: {'; '.join(self.phones)}"
