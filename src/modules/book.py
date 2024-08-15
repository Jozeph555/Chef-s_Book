"""Module for working with Contact Book"""


import os
import json
from datetime import datetime, timedelta
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

    def get_upcoming_birthdays(self, days_ahead=7):
        """
        Returns a list of users whose birthday is within the specified number of days ahead, including the current day.
        """
        current_date = datetime.today().date()

        def get_congratulation_date(birthday: datetime.date) -> datetime.date:
            """ 
            Determines the congratulation date based on the birthday.
            If the birthday falls on a weekend, it moves the congratulation to the next Monday.
            """
            if birthday.weekday() >= 5:  # Saturday or Sunday
                days_to_monday = 7 - birthday.weekday()
                return birthday + timedelta(days=days_to_monday)
            return birthday

        greeting_list = []
        for record in self.data.values():
            try:
                birthdate = datetime.strptime(str(record.birthday), "%d.%m.%Y").date()
                birthdate_this_year = birthdate.replace(year=current_date.year)
                
                # If the birthday has already passed this year, check for next year
                if birthdate_this_year < current_date:
                    birthdate_this_year = birthdate_this_year.replace(year=current_date.year + 1)
                
                days_until_birthday = (birthdate_this_year - current_date).days

                if 0 <= days_until_birthday <= days_ahead:
                    greeting_dict = {
                        "name": record.name.value,
                        "congratulation_date": get_congratulation_date(birthdate_this_year).strftime("%d.%m.%Y")
                    }
                    greeting_list.append(greeting_dict)
            except (AttributeError, ValueError):
                # Skip records without a birthday or with invalid date format
                continue

        return greeting_list

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def save(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

class Record:
    def __init__(self, name, value):
        self.name = name
        self.value = value
