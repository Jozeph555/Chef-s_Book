from typing import List, Optional
from src.modules.error_handler import handle_error, InvalidInputError, RecordNotFoundError
from src.modules.models.customer_model import Customer
from src.modules.service.customers_service import CustomerService
from src.modules.service.bookings_service import BookingsService
from src.modules.ui.commands import get_closest_command, Command

class CustomerManagementCLI:
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

                command, args = get_closest_command(user_input)

                if command in [Command.EXIT, Command.CLOSE]:
                    return self.shutdown()
                elif command == Command.HELLO:
                    self.greet()
                elif command == Command.HELP:
                    self.help()
                elif command == Command.ADD:
                    self.add_customer()
                elif command == Command.EDIT:
                    self.edit_customer()
                elif command == Command.DELETE:
                    self.delete_customer()
                elif command == Command.SHOW:
                    self.show_customer()
                elif command == Command.SHOW_ALL:
                    self.show_all_customers()
                elif command == Command.FIND:
                    self.find_customers()
                elif command == Command.UPCOMING_BIRTHDAY:
                    self.upcoming_birthday()
                elif command == Command.ADD_PHONE:
                    self.add_phone()
                elif command == Command.ADD_NOTE:
                    self.add_note()
                elif command == Command.ADD_TAG:
                    self.add_tag()
                elif command == Command.REMOVE_TAG:
                    self.remove_tag()
                elif command == Command.FIND_TAG:
                    self.find_tag()
                elif command == Command.SORT_TAG:
                    self.sort_tag()
                elif command == Command.RESET:
                    self.reset()
                else:
                    print(f"Unknown command")
        except KeyboardInterrupt:
            self.shutdown()

    def _get_input(self, prompt: str, validator=None, error_message="Invalid input. Please try again or enter 'n' to skip.", allow_empty=False):
        while True:
            value = input(prompt).strip()
            if value.lower() == 'n':
                return None
            if allow_empty and value == "":
                return value
            if not validator or validator(value):
                return value
            print(error_message)

    def _get_customer_name(self) -> Optional[str]:
        while True:
            name = self._get_input("Enter customer name (or 'n' to cancel): ")
            if name is None:
                return None
            customer = self.customer_service.find_by_name(name)
            if customer:
                return name
            print(f"Customer '{name}' not found. Please try again.")

    def add_customer(self):
        customer = Customer()
        
        name = self._get_input("Enter customer name: ", lambda x: len(x) > 0, "Name cannot be empty.")
        if name is None:
            return
        if self.customer_service.find_by_name(name):
            print(f"Customer with name '{name}' already exists.")
            return
        customer.name = name
        print(f"Name added: {name}")

        while True:
            phone = self._get_input("Enter phone number (or 'n' to finish adding phones): ", 
                                    lambda x: x.isdigit() and len(x) == 10, 
                                    "Invalid phone number. Please enter a 10-digit number.")
            if phone is None:
                break
            customer.add_phone(phone)
            print(f"Phone number added to {name}: {phone}")

        birthday = self._get_input("Enter birthday (DD.MM.YYYY) (or 'n' to skip): ", 
                                   lambda x: len(x.split('.')) == 3, 
                                   "Invalid date format. Please use DD.MM.YYYY.")
        if birthday:
            customer.birthday = birthday
            print(f"Birthday added to {name}: {birthday}")

        address = self._get_input("Enter address (or 'n' to skip): ")
        if address:
            customer.address = address
            print(f"Address added to {name}: {address}")

        email = self._get_input("Enter email (or 'n' to skip): ", 
                                lambda x: '@' in x and '.' in x, 
                                "Invalid email format.")
        if email:
            customer.email = email
            print(f"Email added to {name}: {email}")

        self.customer_service.add(customer)
        print(f"Customer {name} added successfully.")

    def edit_customer(self):
        name = self._get_customer_name()
        if name is None:
            return
        customer = self.customer_service.find_by_name(name)[0]
        
        print(f"Editing customer: {name}")
        
        changed = False
        
        new_name = self._get_input(f"Enter new name (current: {customer.name}, press Enter to keep current): ", 
                                allow_empty=True)
        if new_name and new_name != customer.name:
            customer.name = new_name
            print(f"Name updated to: {new_name}")
            changed = True
        
        changed = self._edit_phones(customer) or changed
        changed = self._edit_birthday(customer) or changed
        changed = self._edit_address(customer) or changed
        changed = self._edit_email(customer) or changed
        changed = self._edit_notes(customer) or changed
        
        if changed:
            self.customer_service.save()
            print(f"Customer {customer.name} updated successfully.")
        else:
            print("No changes were made.")

    def _edit_phones(self, customer):
        changed = False
        while True:
            print("Current phone numbers:")
            for i, phone in enumerate(customer.phones):
                print(f"{i}: {phone}")
            action = self._get_input("Enter 'a' to add, 'e' to edit, 'd' to delete a phone, or 'n' to finish editing phones: ")
            if action is None or action.lower() == 'n':
                break
            elif action == 'a':
                phone = self._get_input("Enter new phone number: ", lambda x: x.isdigit() and len(x) == 10, 
                                        "Invalid phone number. Please enter a 10-digit number.")
                if phone:
                    customer.add_phone(phone)
                    print(f"Phone number added: {phone}")
                    changed = True
            elif action == 'e':
                index = self._get_input("Enter the index of the phone to edit: ", lambda x: x.isdigit() and 0 <= int(x) < len(customer.phones),
                                        "Invalid index.")
                if index is not None:
                    index = int(index)
                    new_phone = self._get_input(f"Enter new phone number (current: {customer.phones[index]}): ",
                                                lambda x: x.isdigit() and len(x) == 10,
                                                "Invalid phone number. Please enter a 10-digit number.")
                    if new_phone:
                        customer.phones[index] = new_phone
                        print(f"Phone number updated to: {new_phone}")
                        changed = True
            elif action == 'd':
                index = self._get_input("Enter the index of the phone to delete: ", lambda x: x.isdigit() and 0 <= int(x) < len(customer.phones),
                                        "Invalid index.")
                if index is not None:
                    index = int(index)
                    deleted_phone = customer.phones.pop(index)
                    print(f"Phone number deleted: {deleted_phone}")
                    changed = True
        return changed

    def _edit_birthday(self, customer):
        current_birthday = customer.birthday if customer.birthday else "None"
        new_birthday = self._get_input(f"Enter new birthday (current: {current_birthday}, 'n' to skip, 'd' to delete): ",
                                       lambda x: x == 'd' or len(x.split('.')) == 3,
                                       "Invalid date format. Please use DD.MM.YYYY.")
        if new_birthday == 'd':
            customer.birthday = None
            print("Birthday deleted.")
        elif new_birthday and new_birthday != 'n':
            customer.birthday = new_birthday
            print(f"Birthday updated to: {new_birthday}")

    def _edit_address(self, customer):
        current_address = customer.address if customer.address else "None"
        new_address = self._get_input(f"Enter new address (current: {current_address}, 'n' to skip, 'd' to delete): ")
        if new_address == 'd':
            customer.address = None
            print("Address deleted.")
        elif new_address and new_address != 'n':
            customer.address = new_address
            print(f"Address updated to: {new_address}")

    def _edit_email(self, customer):
        current_email = customer.email if customer.email else "None"
        new_email = self._get_input(f"Enter new email (current: {current_email}, 'n' to skip, 'd' to delete): ",
                                    lambda x: x == 'd' or ('@' in x and '.' in x),
                                    "Invalid email format.")
        if new_email == 'd':
            customer.email = None
            print("Email deleted.")
        elif new_email and new_email != 'n':
            customer.email = new_email
            print(f"Email updated to: {new_email}")

    def _edit_notes(self, customer):
        changed = False
        while True:
            print("Current notes:")
            for i, note in enumerate(customer.notes):
                print(f"{i}: {note.value} (Tags: {', '.join(note.tags)})")
            action = self._get_input("Enter 'a' to add, 'e' to edit, 'd' to delete a note, or 'n' to finish editing notes: ")
            if action is None or action.lower() == 'n':
                break
            elif action == 'a':
                new_note = self._get_input("Enter new note: ")
                if new_note:
                    customer.add_note(new_note)
                    print("Note added.")
                    self._edit_tags(customer, len(customer.notes) - 1)
                    changed = True
            elif action == 'e':
                index = self._get_input("Enter the index of the note to edit: ", lambda x: x.isdigit() and 0 <= int(x) < len(customer.notes),
                                        "Invalid index.")
                if index is not None:
                    index = int(index)
                    new_note = self._get_input(f"Enter new note (current: {customer.notes[index].value}): ")
                    if new_note:
                        customer.notes[index].value = new_note
                        print("Note updated.")
                        self._edit_tags(customer, index)
                        changed = True
            elif action == 'd':
                index = self._get_input("Enter the index of the note to delete: ", lambda x: x.isdigit() and 0 <= int(x) < len(customer.notes),
                                        "Invalid index.")
                if index is not None:
                    index = int(index)
                    deleted_note = customer.notes.pop(index)
                    print(f"Note deleted: {deleted_note.value}")
                    changed = True
        return changed

    def _edit_tags(self, customer, note_index):
        changed = False
        while True:
            print(f"Current tags for note {note_index}: {', '.join(customer.notes[note_index].tags)}")
            action = self._get_input("Enter 'a' to add, 'd' to delete a tag, or 'n' to finish editing tags: ")
            if action == 'a':
                new_tag = self._get_input("Enter new tag: ")
                if new_tag:
                    customer.add_tag_to_note(note_index, new_tag)
                    print(f"Tag '{new_tag}' added.")
                    changed = True
            elif action == 'd':
                tag_to_remove = self._get_input("Enter tag to remove: ")
                if tag_to_remove in customer.notes[note_index].tags:
                    customer.remove_tag_from_note(note_index, tag_to_remove)
                    print(f"Tag '{tag_to_remove}' removed.")
                    changed = True
                else:
                    print(f"Tag '{tag_to_remove}' not found in this note.")
            elif action == 'n':
                break
        return changed

    def delete_customer(self):
        name = self._get_customer_name()
        if name is None:
            return
        customer = self.customer_service.find_by_name(name)[0]
        self.customer_service.delete(customer.id)
        print(f"Customer {name} deleted successfully.")

    def show_customer(self):
        name = self._get_customer_name()
        if name is None:
            return
        customer = self.customer_service.find_by_name(name)[0]
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

    def show_all_customers(self):
        customers = self.customer_service.data
        if not customers:
            print("No customers found.")
        else:
            for customer in customers:
                print(f"{customer.name}: {', '.join(customer.phones) if customer.phones else 'No phone'}")

    def find_customers(self):
        query = self._get_input("Enter search query: ")
        if query is None:
            return
        results = []
        query = query.lower()  # Convert query to lowercase once
        for customer in self.customer_service.data:
            if (query in str(customer.name).lower() or
                any(query in str(phone).lower() for phone in customer.phones) or
                (customer.email and query in str(customer.email).lower())):
                results.append(customer)
        
        if not results:
            print("No matching customers found.")
        else:
            print("Matching customers:")
            for customer in results:
                print(f"{customer.name}: {', '.join(str(phone) for phone in customer.phones) if customer.phones else 'No phone'}")

    def upcoming_birthday(self):
        days = self._get_input("Enter the number of days to check: ", lambda x: x.isdigit(), "Please enter a valid number.")
        if days is None:
            return
        days = int(days)
        upcoming = self.customer_service.customer_birthdays(days)
        if upcoming:
            print(f"Upcoming birthdays in the next {days} days:")
            for customer in upcoming:
                print(f"{customer.name}: {customer.birthday}")
        else:
            print(f"No upcoming birthdays in the next {days} days.")

    def add_phone(self):
        name = self._get_customer_name()
        if name is None:
            return
        customer = self.customer_service.find_by_name(name)[0]
        phone = self._get_input("Enter new phone number: ", lambda x: x.isdigit() and len(x) == 10, 
                                "Invalid phone number. Please enter a 10-digit number.")
        if phone:
            customer.add_phone(phone)
            self.customer_service.save()
            print(f"Phone number {phone} added to customer {name}.")

    def add_note(self):
        name = self._get_customer_name()
        if name is None:
            return
        customer = self.customer_service.find_by_name(name)[0]
        while True:
            note = self._get_input("Enter a note (or 'n' to finish): ")
            if note is None:
                break
            try:
                customer.add_note(note)
                print(f"Note added to customer {name}.")
                
                # Add tags to the note
                while True:
                    tag = self._get_input("Enter a tag for this note (or 'n' to finish adding tags): ")
                    if tag is None:
                        break
                    customer.add_tag_to_note(len(customer.notes) - 1, tag)
                    print(f"Tag '{tag}' added to the note")
            except ValueError as e:
                print(f"Error: {str(e)}")
                print("Please try again.")
        
        self.customer_service.save()

    def add_tag(self):
        name = self._get_customer_name()
        if name is None:
            return
        customer = self.customer_service.find_by_name(name)[0]
        self._show_notes(customer)
        while True:
            note_index = self._get_input("Enter the index of the note to add a tag (or 'n' to finish): ", 
                                         lambda x: x.isdigit() and 0 <= int(x) < len(customer.notes),
                                         "Invalid note index.")
            if note_index is None:
                break
            note_index = int(note_index)
            while True:
                tag = self._get_input("Enter a tag to add (or 'n' to finish adding tags to this note): ")
                if tag is None:
                    break
                customer.add_tag_to_note(note_index, tag)
                print(f"Tag '{tag}' added to note {note_index}")
        self.customer_service.save()

    def remove_tag(self):
        name = self._get_customer_name()
        if name is None:
            return
        customer = self.customer_service.find_by_name(name)[0]
        while True:
            self._show_notes(customer)
            note_index = self._get_input("Enter the index of the note to remove a tag (or 'n' to finish): ", 
                                        lambda x: x.isdigit() and 0 <= int(x) < len(customer.notes),
                                        "Invalid note index.")
            if note_index is None:
                break
            note_index = int(note_index)
            while True:
                print(f"Current tags for note {note_index}: {', '.join(customer.notes[note_index].tags)}")
                tag = self._get_input("Enter a tag to remove (or 'n' to finish removing tags from this note): ")
                if tag is None:
                    break
                if tag in customer.notes[note_index].tags:
                    customer.remove_tag_from_note(note_index, tag)
                    print(f"Tag '{tag}' removed from note {note_index}")
                else:
                    print(f"Tag '{tag}' not found in note {note_index}")
        self.customer_service.save()

    def find_tag(self):
        while True:
            tag = self._get_input("Enter a tag to search for (or 'n' to cancel): ")
            if tag is None:
                break
            results = self.customer_service.find_by_tag(tag)
            if results:
                print(f"Customers with tag '{tag}':")
                for customer in results:
                    print(f"{customer.name}:")
                    for i, note in enumerate(customer.notes):
                        if tag in note.tags:
                            print(f"  Note {i}: {note.value} (Tags: {', '.join(note.tags)})")
            else:
                print(f"No customers found with tag '{tag}'.")

    def sort_tag(self):
        sorted_customers = self.customer_service.sort_by_tags()
        if sorted_customers:
            print("Customers sorted by tags:")
            for customer in sorted_customers:
                print(f"{customer.name}:")
                for i, note in enumerate(customer.notes):
                    if note.tags:
                        print(f"  Note {i}: {note.value} (Tags: {', '.join(note.tags)})")
        else:
            print("No customers with tags found.")

    def _show_notes(self, customer):
        print(f"Notes for {customer.name}:")
        for i, note in enumerate(customer.notes):
            print(f"{i}: {note.value} (Tags: {', '.join(note.tags)})")

    def greet(self):
        print("Hello! How can I assist you today?")

    def reset(self):
        if input("Are you sure you want to reset all data? (y/n): ").lower() != 'y':
            return
        self.customer_service.clear()
        self.bookings_service.clear()
        print("All data has been reset.")

    def shutdown(self):
        self.customer_service.save()
        self.bookings_service.save()
        print("Goodbye!")

    def help(self):
        print("""
        Available commands:
        - hello: Greet the assistant
        - add: Add a new customer
        - edit: Edit an existing customer
        - delete: Delete a customer
        - show: Show details of a customer
        - show-all: Show all customers
        - find: Find customers by name, phone, or email
        - upcoming-birthday: Show customers with upcoming birthdays
        - add-phone: Add a new phone number to an existing customer
        - add-note: Add a new note to an existing customer
        - add-tag: Add a tag to a specific note of a customer
        - remove-tag: Remove a tag from a specific note of a customer
        - find-tag: Find all customers with notes containing the specified tag
        - sort-tag: Show all customers sorted by their tags
        - reset: Reset all saved data
        - exit or close: Exit the program
        """)
