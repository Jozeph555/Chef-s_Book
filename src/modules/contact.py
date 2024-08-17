"""Module for working with Contacts"""


import re
from datetime import datetime, date
from notes import Notes


class Field:
    """Базовий клас для запису поля"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту"""
    def __init__(self, value):
        if len(value) < 3:
            raise ValueError(f"Ім'я '{value}' не було додано. Ім'я має бути довжиною не менше, ніж три літери.")
        else:
            super().__init__(value)


class Email(Field):
    """Клас для зберігання email контакту"""
    def __init__(self, value):
        if not self.is_valid_email(value):
            raise ValueError(f"Email '{value}' не є дійсним.")
        super().__init__(value)

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def __str__(self):
        return f"Email: {self.value}"


class Phone(Field):
    """Клас для зберігання номеру телефону контакту"""
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError(f"Номер телефону {value} не було додано. Номер телефону має містити 10 цифр")
        else:
            super().__init__(value)


class Birthday(Field):
    """
    A class for storing user's birthday
    """
    def __init__(self, value):
        super().__init__(value)
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
            self.validate_date(birthday)
            self.value = birthday
        except ValueError as e:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from e


    def validate_date(self, birthday):
        """
        Checks if the date is not in the future and not earlier than 1900.
        """
        today = date.today()
        if birthday > today:
            raise ValueError("Birthday cannot be in the future")
        if birthday.year < 1900:
            raise ValueError("Birthday year must be 1900 or later")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """"Клас для зберігання інформації про 
    контакт"""
    def __init__(self, name=None) -> None:
        self.name = Name(name) if name else None
        self.phones = []
        self.email = None
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def edit_phone(self, old_phone_number, new_phone_number):
        self.remove_phone(old_phone_number)
        self.add_phone(new_phone_number)

    def remove_phone(self, phone_number):
        for index, p in enumerate(self.phones):
            if p.value == phone_number:
                del self.phones[index]
                return

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_note(self, title, content):
        self.notes.append(Notes(title, content))
