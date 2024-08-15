import json
import os
from collections import UserDict
from contact import Record

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
        return self.data
    
    def display_contact_info(self, name):
        contact = self.find(name)
        if contact:
            return f"Name: {name}, Value: {contact}"
        else:
            return "Contact not found."
    
    def sort_contacts(self, by='name'):
        if by == 'name':
            return dict(sorted(self.data.items()))
        elif by == 'value':
            return dict(sorted(self.data.items(), key=lambda item: item[1]))
        else:
            return "Invalid sort criteria."    
