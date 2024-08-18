from typing import List
from src.modules.error_handler import handle_error, InvalidInputError, RecordNotFoundError
from src.modules.models.customer_model import Customer
from src.modules.service.customers_service import CustomerService
from src.modules.service.bookings_service import BookingsService
from src.modules.ui.command_analyzer import analyze_input


class MainLoop:
    def __init__(self):
        self.customer_service = CustomerService()
        self.bookings_service = BookingsService()

    @handle_error
    def run(self):
        print("Welcome to Chef's Book!")
        try:
            while True:
                user_input = input("Enter a command: ").strip()
                if not user_input:
                    print("Empty input. Please enter a command.")
                    continue

                command, args = analyze_input(user_input)

                if command in ["exit", "close"]:
                    return self.shutdown()
                elif command == "hello":
                    self.greet()
                elif command == "help":
                    self.help()
                elif command == "add":
                    self.add_customer(args)
                elif command == "edit":
                    self.edit_customer(args)
                elif command == "delete":
                    self.delete_customer(args)
                elif command == "show":
                    self.show_customer(args)
                elif command == "show-all":
                    self.show_all_customers()
                elif command == "find":
                    self.find_customers(args)
                elif command == "upcoming-birthday":
                    self.upcoming_birthday(args)
                elif command == "add-phone":
                    self.add_phone(args)
                elif command == "add-note":
                    self.add_note(args)
                elif command == "add-tag":
                    self.add_tag(args)
                elif command == "remove-tag":
                    self.remove_tag(args)
                elif command == "find-tag":
                    self.find_tag(args)
                elif command == "sort-tag":
                    self.sort_tag()
                else:
                    print(f"Unknown command: {command}")
        except KeyboardInterrupt:
            self.shutdown()

    def greet(self):
        print("Hello! How can I assist you today?")

    def shutdown(self):
        self.customer_service.save()
        self.bookings_service.save()
        print("Goodbye!")

    def help(self):
        print("""
        Available commands:
        - hello: Greet the assistant
        - add: Add a new customer
        - edit [name]: Edit an existing customer
        - delete [name]: Delete a customer
        - show [name]: Show details of a customer
        - show-all: Show all customers
        - find [query]: Find customers by name, phone, or email
        - upcoming-birthday [days]: Show customers with birthdays in the next [days] days
        - add-phone [name] [phone]: Add a new phone number to an existing customer
        - add-note [name] [note]: Add a new note to an existing customer
        - add-tag [name] [note_index] [tag]: Add a tag to a specific note of a customer
        - remove-tag [name] [note_index] [tag]: Remove a tag from a specific note of a customer
        - find-tag [tag]: Find all customers with notes containing the specified tag
        - sort-tag: Show all customers sorted by their tags
        - exit or close: Exit the program
        """)

    def _get_input(self, prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty. Please try again.")

    def find_customer(self, name: str) -> Customer:
        customers = self.customer_service.find_by_name(name)
        if not customers:
            raise RecordNotFoundError(f"Customer {name} not found.")
        return customers[0]

    @handle_error
    def add_customer(self, args: List[str]):
        customer = Customer()

        # Name
        name = self._get_input("Enter customer name: ")
        if not name:
            raise InvalidInputError("Name cannot be empty.")
        if self.customer_service.find_by_name(name):
            raise InvalidInputError(f"Customer with name '{name}' already exists.")
        customer.name = name
        print(f"Name added: {name}")

        # Phone (multiple)
        while True:
            phone = self._get_input("Enter phone number (or 'n' to finish adding phones): ")
            if phone.lower() == 'n':
                break
            customer.add_phone(phone)
            print(f"Phone number added to {name}: {phone}")

        # Birthday
        birthday = self._get_input("Enter birthday (DD.MM.YYYY) (or 'n' to skip): ")
        if birthday.lower() != 'n':
            customer.birthday = birthday
            print(f"Birthday added to {name}: {birthday}")

        # Address
        address = self._get_input("Enter address (or 'n' to skip): ")
        if address.lower() != 'n':
            customer.address = address
            print(f"Address added to {name}: {address}")

        # Email
        email = self._get_input("Enter email (or 'n' to skip): ")
        if email.lower() != 'n':
            customer.email = email
            print(f"Email added to {name}: {email}")

        # Notes (multiple)
        while True:
            note = self._get_input("Enter a note (or 'n' to finish adding notes): ")
            if note.lower() == 'n':
                break
            customer.add_note(note)
            print(f"Note added to {name}")

        self.customer_service.add(customer)
        print(f"Customer {name} added successfully.")

    @handle_error
    def edit_customer(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide the name of the customer to edit.")
        name = " ".join(args)
        customer = self.find_customer(name)

        print(f"Editing customer: {name}")

        # Edit name
        new_name = self._get_input(f"Enter new name (current: {customer.name}, press Enter to keep current): ")
        if new_name and new_name != customer.name:
            customer.name = new_name
            print(f"Name updated to: {new_name}")

        # Edit phones
        print("Current phone numbers:")
        for i, phone in enumerate(customer.phones):
            print(f"{i}: {phone}")
        while True:
            action = self._get_input(
                "Enter 'a' to add, 'e' to edit, 'd' to delete a phone, or 'n' to finish editing phones: ")
            if action.lower() == 'a':
                new_phone = self._get_input("Enter new phone number: ")
                customer.add_phone(new_phone)
                print(f"Phone number added: {new_phone}")
            elif action.lower() == 'e':
                index = int(self._get_input("Enter the index of the phone to edit: "))
                if 0 <= index < len(customer.phones):
                    new_phone = self._get_input(f"Enter new phone number (current: {customer.phones[index]}): ")
                    customer.phones[index] = new_phone
                    print(f"Phone number updated to: {new_phone}")
                else:
                    print("Invalid index.")
            elif action.lower() == 'd':
                index = int(self._get_input("Enter the index of the phone to delete: "))
                if 0 <= index < len(customer.phones):
                    deleted_phone = customer.phones.pop(index)
                    print(f"Phone number deleted: {deleted_phone}")
                else:
                    print("Invalid index.")
            elif action.lower() == 'n':
                break

        # Edit birthday
        current_birthday = customer.birthday if customer.birthday else "None"
        new_birthday = self._get_input(
            f"Enter new birthday (current: {current_birthday}, 'n' to skip, 'd' to delete): ")
        if new_birthday.lower() == 'd':
            customer.birthday = None
            print("Birthday deleted.")
        elif new_birthday.lower() != 'n':
            customer.birthday = new_birthday
            print(f"Birthday updated to: {new_birthday}")

        # Edit address
        current_address = customer.address if customer.address else "None"
        new_address = self._get_input(f"Enter new address (current: {current_address}, 'n' to skip, 'd' to delete): ")
        if new_address.lower() == 'd':
            customer.address = None
            print("Address deleted.")
        elif new_address.lower() != 'n':
            customer.address = new_address
            print(f"Address updated to: {new_address}")

        # Edit email
        current_email = customer.email if customer.email else "None"
        new_email = self._get_input(f"Enter new email (current: {current_email}, 'n' to skip, 'd' to delete): ")
        if new_email.lower() == 'd':
            customer.email = None
            print("Email deleted.")
        elif new_email.lower() != 'n':
            customer.email = new_email
            print(f"Email updated to: {new_email}")

        # Edit notes
        print("Current notes:")
        for i, note in enumerate(customer.notes):
            print(f"{i}: {note}")
        while True:
            action = self._get_input(
                "Enter 'a' to add, 'e' to edit, 'd' to delete a note, or 'n' to finish editing notes: ")
            if action.lower() == 'a':
                new_note = self._get_input("Enter new note: ")
                customer.add_note(new_note)
                print("Note added.")
            elif action.lower() == 'e':
                index = int(self._get_input("Enter the index of the note to edit: "))
                if 0 <= index < len(customer.notes):
                    new_note = self._get_input(f"Enter new note (current: {customer.notes[index]}): ")
                    customer.notes[index] = new_note
                    print("Note updated.")
                else:
                    print("Invalid index.")
            elif action.lower() == 'd':
                index = int(self._get_input("Enter the index of the note to delete: "))
                if 0 <= index < len(customer.notes):
                    deleted_note = customer.notes.pop(index)
                    print(f"Note deleted: {deleted_note}")
                else:
                    print("Invalid index.")
            elif action.lower() == 'n':
                break

        self.customer_service.save()
        print(f"Customer {customer.name} updated successfully.")

    @handle_error
    def delete_customer(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide the name of the customer to delete.")
        name = " ".join(args)
        customer = self.find_customer(name)
        self.customer_service.delete(customer.id)
        print(f"Customer {name} deleted successfully.")

    @handle_error
    def show_customer(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide the name of the customer to show.")
        name = " ".join(args)
        customer = self.find_customer(name)
        print(f"Customer details for {customer.name}:")
        print("Phone numbers:")
        for i, phone in enumerate(customer.phones):
            print(f"{i}: {phone}")
        print(f"Birthday: {customer.birthday if customer.birthday else 'None'}")
        print(f"Address: {customer.address if customer.address else 'None'}")
        print(f"Email: {customer.email if customer.email else 'None'}")
        print("Notes:")
        for i, note in enumerate(customer.notes):
            print(f"{i}: {note.value} (Tags: {', '.join(note.tags)})")

    @handle_error
    def show_all_customers(self):
        customers = self.customer_service.data
        if not customers:
            print("No customers found.")
        else:
            for customer in customers:
                print(f"{customer.name}: {', '.join(customer.phones) if customer.phones else 'No phone'}")

    @handle_error
    def find_customers(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide a search query.")
        query = " ".join(args).lower()
        results = []
        for customer in self.customer_service.data:
            if (query in str(customer.name).lower() or
                    any(query in phone.lower() for phone in customer.phones) or
                    (customer.email and query in str(customer.email).lower())):
                results.append(customer)

        if not results:
            print("No matching customers found.")
        else:
            print("Matching customers:")
            for customer in results:
                print(f"{customer.name}: {', '.join(customer.phones) if customer.phones else 'No phone'}")

    @handle_error
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

    @handle_error
    def add_phone(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide the name of the customer and the phone number to add.")
        name = " ".join(args[:-1])
        phone = args[-1]
        customer = self.find_customer(name)
        customer.add_phone(phone)
        self.customer_service.save()
        print(f"Phone number {phone} added to customer {name}.")

    @handle_error
    def add_note(self, args: List[str]):
        if len(args) < 2:
            raise InvalidInputError("Please provide the name of the customer and the note to add.")
        name = args[0]
        note = " ".join(args[1:])
        customer = self.find_customer(name)
        customer.add_note(note)
        self.customer_service.save()
        print(f"Note added to customer {name}.")

    @handle_error
    def add_tag(self, args: List[str]):
        if len(args) < 3:
            raise InvalidInputError("Please provide the name of the customer, note index, and tag.")
        name = args[0]
        try:
            note_index = int(args[1])
        except ValueError:
            raise InvalidInputError("Note index must be a number.")
        tag = args[2]
        customer = self.find_customer(name)
        if 0 <= note_index < len(customer.notes):
            customer.notes[note_index].add_tag(tag)
            self.customer_service.save()
            print(f"Tag '{tag}' added to note {note_index} for customer {name}.")
        else:
            raise InvalidInputError(f"Invalid note index for customer {name}.")

    @handle_error
    def remove_tag(self, args: List[str]):
        if len(args) < 3:
            raise InvalidInputError("Please provide the name of the customer, note index, and tag.")
        name = args[0]
        try:
            note_index = int(args[1])
        except ValueError:
            raise InvalidInputError("Note index must be a number.")
        tag = args[2]
        customer = self.find_customer(name)
        if 0 <= note_index < len(customer.notes):
            if tag in customer.notes[note_index].tags:
                customer.notes[note_index].remove_tag(tag)
                self.customer_service.save()
                print(f"Tag '{tag}' removed from note {note_index} for customer {name}.")
            else:
                print(f"Tag '{tag}' not found in note {note_index} for customer {name}.")
        else:
            raise InvalidInputError(f"Invalid note index for customer {name}.")

    def find_tag(self, args: List[str]):
        if len(args) < 1:
            raise InvalidInputError("Please provide a tag to search for.")
        tag = args[0]
        results = self.customer_service.find_by_tag(tag)
        if results:
            print(f"Customers with tag '{tag}':")
            for customer in results:
                print(customer.name)
        else:
            print(f"No customers found with tag '{tag}'.")

    def sort_tag(self):
        sorted_customers = self.customer_service.sort_by_tags()
        if sorted_customers:
            print("Customers sorted by tags:")
            for customer in sorted_customers:
                print(f"{customer.name}: {', '.join(tag for note in customer.notes for tag in note.tags)}")
        else:
            print("No customers with tags found.")
