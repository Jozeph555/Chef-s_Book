from src.modules.models.fields.base_field import Field


class PhoneField(Field):
    LENGTH = 10

    def __init__(self, value=None, validate=True):
        super().__init__(value, validate)

    def _validate(self, value):
        if not value.isdigit():
            raise ValueError(f"The phone number '{value}' was not added. "
                             f"The phone number must contain only digits.")
        if len(value) != PhoneField.LENGTH:
            raise ValueError(f"The phone number '{value}' was not added. "
                             f"The phone number must contain {PhoneField.LENGTH} digits.")
