import unittest

from src.modules.models.customer_model import AddressField


class TestAddress(unittest.TestCase):
    def test_valid_address(self):
        address = AddressField("Some Street, Some Town, Somewhere")
        self.assertEqual(address.value, "Some Street, Some Town, Somewhere")

    def test_invalid_address_length(self):
        with self.assertRaises(ValueError):
            AddressField("A")

    def test_invalid_address_format(self):
        with self.assertRaises(ValueError):
            AddressField("Some Street")
