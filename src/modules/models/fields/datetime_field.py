from datetime import datetime

from src.modules.models.fields.base_field import Field


class DatetimeField(Field):
    FORMAT = "%d.%m.%Y %H:%M"

    def __init__(self, value=None, validate=True):
        super().__init__(value, validate)

    def __str__(self):
        return self.value.strftime(DatetimeField.FORMAT)

    def _validate(self, value):
        try:
            self._parse(value)
        except ValueError:
            raise ValueError(f"Invalid date format. Use {DatetimeField.FORMAT}")

    def _parse(self, value):
        return datetime.strptime(value, DatetimeField.FORMAT).date()
