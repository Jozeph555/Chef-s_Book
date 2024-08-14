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
    
class Email(Field):
    pass


class Record:
    """"Клас для зберігання інформації про 
    контакт"""
    def __init__(self, name=None) -> None:
        self.name = Name(name) if name else None
        self.phones = []
        self.email = None
        self.birthday = None

    def to_dict(self):
        return {
            'name': self.name,
            'phones':[phone.value for phone in self.phones], #if self.phones else []
            "email": self.email,
            'birthday': self.birthday
        }
    
    def from_dict(self, data: dict):
        self.name = Name(data.get("name"))
        self.phones = [Phone(phone) for phone in data.get("phones")]
        self.email = Email(data.get("email")) 
        self.birthday = Birthday(data.get("birthday"))   
