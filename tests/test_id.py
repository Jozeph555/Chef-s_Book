import unittest

from src.modules.models.fields.id_field import IDField


class TestIDField(unittest.TestCase):
    def test_valid_name(self):
        name = IDField("2")
        self.assertEqual(name.value, "2")
        self.assertEqual(str(name), "2")
