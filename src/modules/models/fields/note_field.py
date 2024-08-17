from src.modules.models.fields.base_field import Field


class NoteField(Field):
    MIN_LENGTH = 3
    MAX_LENGTH = 255

    def __init__(self, value=None, tags=None, validate=True):
        super().__init__(value, validate)
        self.tags = tags or []

    def _validate(self, value):
        if not NoteField.MIN_LENGTH <= len(value) <= NoteField.MAX_LENGTH:
            raise ValueError(
                f"The note '{value}' was not added. "
                f"The note must be between {NoteField.MIN_LENGTH} and {NoteField.MAX_LENGTH} characters long.")

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
