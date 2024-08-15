"""Module for working with contacts"""

from datetime import datetime


class Field:
    """Base class for fields of contacts"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing the name of the contact"""

    def __init__(self, value):
        if len(value) < 3:
            raise ValueError(f"The name '{value}' was not added. The name must be at least three characters long.")
        else:
            super().__init__(value)


class Phone(Field):
    """Class for storing the phone number of the contact"""

    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError(f"The phone number {value} was not added. The phone number must contain 10 digits.")
        else:
            super().__init__(value)


class Birthday(Field):
    """Class for storing the birthday of the contact"""

    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Incorrect date format. Use DD.MM.YYYY")
        super().__init__(parsed_date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Class for storing information about a contact"""
    pass
