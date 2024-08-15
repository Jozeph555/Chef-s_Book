"""Модуль для роботи з Контактами"""


from datetime import datetime


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


class Phone(Field):
    """Клас для зберігання номеру телефону контакту"""
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError(f"Номер телефону {value} не було додано. Номер телефону має містити 10 цифр")
        else:
            super().__init__(value)


class Birthday(Field):
    """Клас для зберігання дня народження контакту"""
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Неправильний формат дати. Використовуйте ДД.ММ.РРРР")
        super().__init__(parsed_date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """"Клас для зберігання інформації про 
    контакт"""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.notes = []

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
