import unittest

from src.modules.dto.customer_dto import CustomerDTO
from src.modules.models.customer_model import Customer

TEST_PHONE = '0000000000'
TEST_NAME = 'TEST'


class TestCustomerModel(unittest.TestCase):
    def test_create_record(self):
        record = Customer()
        record.name = TEST_NAME
        self.assertEqual(record.name, TEST_NAME)
        self.assertEqual(record.phones, [])
        self.assertIsNone(record.birthday)
        self.assertIsNone(record.address)
        self.assertIsNone(record.email)

    def test_add_phone(self):
        record = Customer()
        record.add_phone(TEST_PHONE)
        self.assertIn(TEST_PHONE, record.phones)

    def test_find_phone(self):
        record = Customer()
        record.add_phone(TEST_PHONE)
        self.assertEqual(record.has_phone(TEST_PHONE), True)
        self.assertEqual(record.has_phone("0987654321"), False)

    def test_edit_phone(self):
        record = Customer()
        record.edit_phone(TEST_PHONE, "1234567890")
        self.assertEqual(record.has_phone("1234567890"), True)
        self.assertEqual(record.has_phone(TEST_PHONE), False)

    def test_remove_phone(self):
        record = Customer()
        record.remove_phone(TEST_PHONE)
        self.assertIs(record.has_phone(TEST_PHONE), False)

    def test_set_get_birthday(self):
        record = Customer()
        record.birthday = "01.01.2000"
        self.assertEqual(record.birthday, "01.01.2000")

    def test_set_get_address(self):
        record = Customer()
        record.address = "Some Street, Some Town, Somewhere"
        self.assertEqual(record.address, "Some Street, Some Town, Somewhere")

    def test_set_get_email(self):
        record = Customer()
        record.email = "test.test@test.com"
        self.assertEqual(record.email, "test.test@test.com")
        with self.assertRaises(ValueError):
            record.email = "test"

    def test_to_dto(self):
        record = Customer()
        record.name = TEST_NAME
        record.add_phone(TEST_PHONE)
        record.birthday = "01.01.2000"
        record.address = "Some Street, Some Town, Somewhere"
        record.email = "test@test.com"

        dto = record.dto()

        self.assertIsNotNone(dto.id)
        self.assertEqual(dto.name, TEST_NAME)
        self.assertEqual(dto.phones, [TEST_PHONE])
        self.assertEqual(dto.birthday, "01.01.2000")
        self.assertEqual(dto.address, "Some Street, Some Town, Somewhere")
        self.assertEqual(dto.email, "test@test.com")

    def test_from_dto(self):
        dto = CustomerDTO(
            id='test',
            name=TEST_NAME,
            phones=[TEST_PHONE],
            birthday="01.01.2000",
            address="Some Street, Some Town, Somewhere",
            email="test@test.com"
        )

        record = Customer(dto)

        self.assertEqual(record.name, TEST_NAME)
        self.assertIn(TEST_PHONE, record.phones)
        self.assertEqual(record.birthday, "01.01.2000")
        self.assertEqual(record.address, "Some Street, Some Town, Somewhere")
        self.assertEqual(record.email, "test@test.com")


if __name__ == '__main__':
    unittest.main()
