from src.modules.models.fields.base_field import Field


class NameField(Field):
    MIN_LENGTH = 3
    MAX_LENGTH = 40

    def __init__(self, value=None, validate=True):
        super().__init__(value, validate)

    def _validate(self, value):
        if not NameField.MIN_LENGTH <= len(value) <= NameField.MAX_LENGTH:
            raise ValueError(f"The name '{value}' was not added. "
                             f"The name must be between {NameField.MIN_LENGTH} and {NameField.MAX_LENGTH} characters long.")

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        elif isinstance(other, NameField):
            return self.value == other.value
        return False
