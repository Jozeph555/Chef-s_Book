import json
import os
from collections import UserDict

class ContactBook(UserDict):
    def __init__(self, filename='contacts.json'):
        super().__init__()
        self.filename = filename
        self.load()

    def add_record(self, record):
        self.data[record.name] = record.value
        self.save()

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            self.save()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def save(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def list_contacts(self):
        return [f"{name}: {info}" for name, info in self.data.items()]

    def sort_contacts(self, key=None):
        return sorted(self.data.items(), key=lambda item: item[1].get(key) if key else item[0])

    def display_contacts(self):
        for name, info in self.data.items():
            print(f"Name: {name}, Info: {info}")

    def sort_and_display_contacts(self, key=None):
        sorted_contacts = self.sort_contacts(key)
        for name, info in sorted_contacts:
            print(f"Name: {name}, Info: {info}")

class Record:
    def __init__(self, name, value):
        self.name = name
        self.value = value
