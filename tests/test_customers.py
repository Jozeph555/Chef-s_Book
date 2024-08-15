import unittest

from src.modules.service.customers_service import CustomerService
from src.modules.models.customer_model import Customer


class TestCustomers(unittest.TestCase):

    def setUp(self):
        self.customers = CustomerService()

        self.customer1 = Customer()
        self.customer1.name = "Test"
        self.customer1.birthday = "01.01.2000"

        self.customer2 = Customer()
        self.customer2.name = "Test2"
        self.customer2.birthday = "01.01.2000"

        self.customers.add(self.customer1)
        self.customers.add(self.customer2)

    def tearDown(self):
        self.customers.clear()

    def test_add_customer(self):
        self.assertEqual(len(self.customers), 2)
        self.assertIsNotNone(self.customers.find(self.customer1.id))
        self.assertIsNotNone(self.customers.find(self.customer2.id))

    def test_find_customer(self):
        customer = self.customers.find(self.customer1.id)
        self.assertEqual(customer.name, "Test")
        self.assertIsNone(self.customers.find("NONEXISTENT"))

    def test_delete_customer(self):
        self.customers.delete(self.customer2.id)
        self.assertIsNone(self.customers.find(self.customer2.id))
        self.assertEqual(len(self.customers), 1)


if __name__ == "__main__":
    unittest.main()
