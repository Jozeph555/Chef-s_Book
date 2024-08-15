import unittest

from src.modules.models.fields.name_field import NameField


class TestName(unittest.TestCase):
    def test_valid_name(self):
        name = NameField("Test")
        self.assertEqual(name.value, "Test")

    def test_invalid_name_length(self):
        with self.assertRaises(ValueError):
            NameField("Te")
        with self.assertRaises(ValueError):
            NameField("T" * 100)
