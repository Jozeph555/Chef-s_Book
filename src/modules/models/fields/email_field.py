import re

from src.modules.models.fields.base_field import Field


class EmailField(Field):
    EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")

    def __init__(self, value=None, validate=True):
        super().__init__(value, validate)

    def _validate(self, value):
        if not EmailField.EMAIL_PATTERN.match(value):
            raise ValueError(f"The email '{value}' was not added. The email must be in a valid format.")
