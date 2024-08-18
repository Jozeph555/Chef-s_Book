"""Module for interaction with the user interface"""


from typing import List
from datetime import datetime, timedelta
from src.modules.service.customers_service import CustomerService
from src.modules.service.bookings_service import BookingsService
from src.modules.ui.command_analyzer import analyze_input
from src.modules.error_handler import handle_error, InvalidInputError, RecordNotFoundError
from src.modules.models.customer_model import Customer

class MainLoop:
    def __init__(self):
        self.customer_service = CustomerService()
        self.bookings_service = BookingsService()

    @handle_error
    def run(self):
        print("Welcome to Chef's Book!")
        while True:
            user_input = input("Enter a command: ")
            command, args = analyze_input(user_input)

            if not user_input.strip():
                print("Empty input. Please enter a command.")
                continue

            if command in ["exit", "close"]:
                print("Goodbye!")
                break
            elif command == "hello":
                self.hello()
            elif command == "add":
                self.add_customer(args)
            elif command == "add-phone":
                self.add_phone(args)
            elif command == "edit-phone":
                self.edit_phone(args)
            elif command == "remove-phone":
                self.remove_phone(args)
            elif command == "has-phone":
                self.has_phone(args)
            elif command == "add-note":
                self.add_note(args)
            elif command == "edit-note":
                self.edit_note(args)
            elif command == "remove-note":
                self.remove_note(args)
            elif command == "has-note":
                self.has_note(args)
            elif command == "add-tag":
                self.add_tag(args)
            elif command == "remove-tag":
                self.remove_tag(args)
            elif command == "find-tag":
                self.find_tag(args)
            elif command == "sort-tag":
                self.sort_tag()
            elif command == "show-all":
                self.show_all()
            elif command == "add-birthday":
                self.add_birthday(args)
            elif command == "show-birthday":
                self.show_birthday(args)
            elif command == "upcoming-birthday":
                self.upcoming_birthday(args)
            elif command == "add-email":
                self.add_email(args)
            elif command == "show-email":
                self.show_email(args)
            elif command == "add-address":
                self.add_address(args)
            elif command == "show-address":
                self.show_address(args)
            elif command == "show-notes":
                self.show_notes(args)
            else:
                print(f"Unknown command: {command}")
            
            print('Ready for the next command')

    def hello(self):
        print("How can I help you?")

    def add_customer(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide a name for the customer.")
        name = " ".join(args)
        if self.customer_service.find_by_name(name):
            raise InvalidInputError(f"Customer with name '{name}' already exists.")
        customer = Customer()
        customer.name = name
        self.customer_service.add(customer)
        print(f"Customer {name} added successfully.")

    def add_phone(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide customer name and phone number.")
        name, phone = " ".join(args[:-1]), args[-1]
        customer = self.find_customer(name)
        if customer.has_phone(phone):
            raise InvalidInputError(f"Phone {phone} already exists for {name}.")
        customer.add_phone(phone)
        self.customer_service.save()
        print(f"Phone {phone} added to {name}.")

    def edit_phone(self, args: List[str]):
        if len(args) < 3:
            raise InvalidInputError("Please provide customer name, old phone, and new phone.")
        name, old_phone, new_phone = " ".join(args[:-2]), args[-2], args[-1]
        customer = self.find_customer(name)
        if not customer.has_phone(old_phone):
            raise InvalidInputError(f"Phone {old_phone} not found for {name}.")
        if customer.has_phone(new_phone):
            raise InvalidInputError(f"Phone {new_phone} already exists for {name}.")
        customer.edit_phone(old_phone, new_phone)
        self.customer_service.save()
        print(f"Phone changed from {old_phone} to {new_phone} for {name}.")

    def remove_phone(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide customer name and phone number.")
        name, phone = " ".join(args[:-1]), args[-1]
        customer = self.find_customer(name)
        customer.remove_phone(phone)
        self.customer_service.save()
        print(f"Phone {phone} removed from {name}.")

    def has_phone(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide customer name and phone number.")
        name, phone = " ".join(args[:-1]), args[-1]
        customer = self.find_customer(name)
        if customer.has_phone(phone):
            print(f"{name} has the phone number {phone}.")
        else:
            print(f"{name} does not have the phone number {phone}.")

    def add_note(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide customer name and note.")
        name, note = args[0], " ".join(args[1:])
        customer = self.find_customer(name)
        customer.add_note(note)
        self.customer_service.save()
        print(f"Note added to {name}.")

    def edit_note(self, args: List[str]):
        if len(args) < 3:
            raise InvalidInputError("Please provide customer name, note index, and new note.")
        name, index, new_note = args[0], int(args[1]), " ".join(args[2:])
        customer = self.find_customer(name)
        if index < 0 or index >= len(customer.notes):
            raise InvalidInputError(f"Invalid note index for {name}.")
        customer.notes[index] = NoteField(new_note)
        self.customer_service.save()
        print(f"Note {index} edited for {name}.")

    def remove_note(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide customer name and note index.")
        name, index = args[0], int(args[1])
        customer = self.find_customer(name)
        if index < 0 or index >= len(customer.notes):
            raise InvalidInputError(f"Invalid note index for {name}.")
        del customer.notes[index]
        self.customer_service.save()
        print(f"Note {index} removed from {name}.")

    def has_note(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide customer name and note content.")
        name, content = args[0], " ".join(args[1:])
        customer = self.find_customer(name)
        if customer.has_note(content):
            print(f"{name} has a note containing '{content}'.")
        else:
            print(f"{name} does not have a note containing '{content}'.")

    def add_tag(self, args: List[str]):
        if len(args) < 3:
            raise InvalidInputError("Please provide customer name, note index, and tag.")
        name, index, tag = args[0], int(args[1]), args[2]
        customer = self.find_customer(name)
        if index < 0 or index >= len(customer.notes):
            raise InvalidInputError(f"Invalid note index for {name}.")
        customer.notes[index].add_tag(tag)
        self.customer_service.save()
        print(f"Tag '{tag}' added to note {index} for {name}.")

    def remove_tag(self, args: List[str]):
        if len(args) < 3:
            raise InvalidInputError("Please provide customer name, note index, and tag.")
        name, index, tag = args[0], int(args[1]), args[2]
        customer = self.find_customer(name)
        if index < 0 or index >= len(customer.notes):
            raise InvalidInputError(f"Invalid note index for {name}.")
        if tag not in customer.notes[index].tags:
            raise InvalidInputError(f"Tag '{tag}' not found in note {index} for {name}.")
        customer.notes[index].remove_tag(tag)
        self.customer_service.save()
        print(f"Tag '{tag}' removed from note {index} for {name}.")

    def find_tag(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide a tag to search for.")
        tag = args[0]
        customers = self.customer_service.find_by_tag(tag)
        if customers:
            print(f"Customers with tag '{tag}':")
            for customer in customers:
                print(customer)
        else:
            print(f"No customers found with tag '{tag}'.")

    def sort_tag(self):
        sorted_customers = self.customer_service.sort_by_tags()
        print("Customers sorted by tags:")
        for customer in sorted_customers:
            print(customer)

    def show_all(self):
        customers = self.customer_service.data
        if customers:
            print("All customers:")
            for customer in customers:
                print(customer)
        else:
            print("No customers found.")

    def add_birthday(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide customer name and birthday (DD.MM.YYYY).")
        name, birthday = " ".join(args[:-1]), args[-1]
        customer = self.find_customer(name)
        customer.birthday = birthday
        self.customer_service.save()
        print(f"Birthday {birthday} added to {name}.")

    def show_birthday(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide customer name.")
        name = " ".join(args)
        customer = self.find_customer(name)
        if customer.birthday:
            print(f"{name}'s birthday is {customer.birthday}.")
        else:
            print(f"{name} has no birthday set.")

    def upcoming_birthday(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide the number of days to check.")
        days = int(args[0])
        upcoming = self.customer_service.customer_birthdays(days)
        if upcoming:
            print(f"Upcoming birthdays in the next {days} days:")
            for customer in upcoming:
                print(f"{customer.name}: {customer.birthday}")
        else:
            print(f"No upcoming birthdays in the next {days} days.")

    def add_email(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide customer name and email.")
        name, email = " ".join(args[:-1]), args[-1]
        customer = self.find_customer(name)
        customer.email = email
        self.customer_service.save()
        print(f"Email {email} added to {name}.")

    def show_email(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide customer name.")
        name = " ".join(args)
        customer = self.find_customer(name)
        if customer.email:
            print(f"{name}'s email is {customer.email}.")
        else:
            print(f"{name} has no email set.")

    def add_address(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide customer name and address.")
        name, address = args[0], " ".join(args[1:])
        customer = self.find_customer(name)
        customer.address = address
        self.customer_service.save()
        print(f"Address added to {name}.")

    def show_address(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide customer name.")
        name = " ".join(args)
        customer = self.find_customer(name)
        if customer.address:
            print(f"{name}'s address is {customer.address}.")
        else:
            print(f"{name} has no address set.")

    def show_notes(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide customer name.")
        name = " ".join(args)
        customer = self.find_customer(name)
        if customer.notes:
            print(f"Notes for {name}:")
            for i, note in enumerate(customer.notes):
                print(f"{i}: {note.value} (Tags: {', '.join(note.tags)})")
        else:
            print(f"{name} has no notes.")

    def find_customer(self, name: str) -> Customer:
        customer = self.customer_service.find_by_name(name)
        if not customer:
            raise RecordNotFoundError(f"Customer {name} not found.")
        return customer[0]  # Assuming find_by_name returns a list
