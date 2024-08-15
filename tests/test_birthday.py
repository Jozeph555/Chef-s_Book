import unittest
from datetime import datetime

from src.modules.models.fields.date_field import DateField


class TestBirthday(unittest.TestCase):
    def test_valid_birthday(self):
        birthday = DateField("01.01.2000")
        self.assertEqual(birthday.value, datetime.strptime("01.01.2000", "%d.%m.%Y").date())

    def test_invalid_birthday_format(self):
        with self.assertRaises(ValueError):
            DateField("tomorrow")
        with self.assertRaises(ValueError):
            DateField("01-01-2000")
