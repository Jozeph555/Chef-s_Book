import unittest

from src.modules.models.fields.phone_field import PhoneField


class TestPhone(unittest.TestCase):
    def test_valid_phone(self):
        phone = PhoneField("0000000000")
        self.assertEqual(phone.value, "0000000000")

    def test_invalid_phone(self):
        with self.assertRaises(ValueError):
            PhoneField("000000X000")
        with self.assertRaises(ValueError):
            PhoneField("00000000")
