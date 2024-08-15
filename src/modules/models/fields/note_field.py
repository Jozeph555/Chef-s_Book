from src.modules.models.fields.base_field import Field


class NoteField(Field):
    MIN_LENGTH = 3
    MAX_LENGTH = 255

    def __init__(self, value=None, validate=True):
        super().__init__(value, validate)

    def _validate(self, value):
        if not NoteField.MIN_LENGTH <= len(value) <= NoteField.MAX_LENGTH:
            raise ValueError(
                f"The note '{value}' was not added."
                f"The note must be between {NoteField.MIN_LENGTH} and {NoteField.MAX_LENGTH} characters long.")
