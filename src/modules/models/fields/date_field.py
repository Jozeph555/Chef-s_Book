from datetime import datetime

from src.modules.models.fields.base_field import Field


class DateField(Field):
    FORMAT = "%d.%m.%Y"

    def __init__(self, value=None, validate=True):
        super().__init__(value, validate)

    def __str__(self):
        return self.value.strftime(DateField.FORMAT)

    def _validate(self, value):
        try:
            self._parse(value)
        except ValueError:
            raise ValueError(f"Invalid date format. Use {DateField.FORMAT}")

    def _parse(self, value):
        return datetime.strptime(value, DateField.FORMAT).date()
