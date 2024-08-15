import unittest
import os

from src.modules.dto.base_dto import BaseDTO
from src.modules.storage import Storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.filename = "test_storage.csv"
        self.storage = Storage(BaseDTO, self.filename)
        self.dto1 = BaseDTO(id="1")
        self.dto2 = BaseDTO(id="2")
        self.test_data = [self.dto1, self.dto2]

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_and_load(self):
        self.storage.save(self.test_data)

        loaded_data = self.storage.load()

        self.assertEqual(loaded_data, self.test_data)

    def test_load_empty_file(self):
        loaded_data = self.storage.load()

        self.assertEqual(loaded_data, [])

    def test_file_not_created_on_empty_save(self):
        self.storage.save([])

        self.assertFalse(os.path.exists(self.filename))


if __name__ == '__main__':
    unittest.main()
