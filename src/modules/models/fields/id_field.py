import uuid

from src.modules.models.fields.base_field import Field


class IDField(Field):
    def __init__(self, value=None):
        if value is None:
            value = uuid.uuid4()
        super().__init__(value)

    def __str__(self):
        return str(self.value)
