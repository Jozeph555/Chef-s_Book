class Field():
    """Base field class"""

    def __init__(self, value=None, validate=True):
        if validate:
            self._validate(value)
        if not (value is None):
            self.value = self._parse(value)
        else:
            self.value = value

    def __str__(self):
        return str(self.value)

    def _validate(self, value):
        """Method to validate the input value"""
        pass

    def _parse(self, value):
        """Method to parse the input value (if needed)"""
        return value
