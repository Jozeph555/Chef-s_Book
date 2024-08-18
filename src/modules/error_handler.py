"""Еrror handling module"""


class ChefBookError(Exception):
    """Base exception for Chef's Book"""

class InvalidInputError(ChefBookError):
    """Raised when the input is invalid"""

class RecordNotFoundError(ChefBookError):
    """Raised when a record is not found"""

class DuplicateRecordError(ChefBookError):
    """Raised when trying to add a duplicate record"""

def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ChefBookError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
    return wrapper
