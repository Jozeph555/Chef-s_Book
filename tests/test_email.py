import unittest

from src.modules.models.customer_model import EmailField


class TestEmail(unittest.TestCase):
    def test_valid_email(self):
        EmailField("test.test@test.com")
        email = EmailField("test@test.com")
        self.assertEqual(email.value, "test@test.com")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            EmailField("test")
        with self.assertRaises(ValueError):
            EmailField("test@test")
