from src.modules.models.fields.base_field import Field


class AddressField(Field):
    MIN_LENGTH = 3
    MAX_LENGTH = 255

    def __init__(self, value=None, validate=True):
        super().__init__(value, validate)

    def _validate(self, value):
        if not AddressField.MIN_LENGTH <= len(value) <= AddressField.MAX_LENGTH:
            raise ValueError(
                f"The address '{value}' was not added. "
                f"The address must be between {AddressField.MIN_LENGTH} and {AddressField.MAX_LENGTH} characters long.")

        components = value.split(',')
        if not len(components) >= 2 and all(component.strip() for component in components):
            raise ValueError(
                f"The address '{value}' was not added. "
                f"Format of the address should be: '[Address Line 1], [City], [Country]'.")
