import json
import os

class AddressBook:
    def __init__(self, filename='address_book.json'):
        self.filename = filename
        self.contacts = {}
        if os.path.exists(self.filename):
            self.load()
        else:
            self.save()

    def add_contact(self, name, address, phone):
        self.contacts[name] = {'address': address, 'phone': phone}
        self.save()

    def remove_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            self.save()

    def get_contact(self, name):
        return self.contacts.get(name, None)

    def save(self):
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def load(self):
        with open(self.filename, 'r') as file:
            self.contacts = json.load(file)

# Приклад використання
if __name__ == "__main__":
    book = AddressBook()
  