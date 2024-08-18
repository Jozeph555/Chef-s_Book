from datetime import datetime
from typing import List, Tuple, Optional

from src.modules.dto.customer_dto import CustomerDTO
from src.modules.models.fields.address_field import AddressField
from src.modules.models.fields.date_field import DateField
from src.modules.models.fields.email_field import EmailField
from src.modules.models.fields.id_field import IDField
from src.modules.models.fields.name_field import NameField
from src.modules.models.fields.phone_field import PhoneField
from src.modules.models.fields.note_field import NoteField


class Customer:
    """Class for storing customer info"""

    def __init__(self, dto: CustomerDTO = None):
        if not dto:
            dto = CustomerDTO()

        self._id = IDField(dto.id)
        self._name = NameField(dto.name, validate=False)
        self._birthday = DateField(dto.birthday, validate=False)
        self._address = AddressField(dto.address, validate=False)
        self._email = EmailField(dto.email, validate=False)
        self._phones = [PhoneField(phone, validate=False) for phone in dto.phones]
        self._notes = [NoteField(note, validate=False) for note in dto.notes]

    @property
    def id(self) -> str:
        return str(self._id)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = NameField(name)

    @property
    def phones(self) -> List[str]:
        return [phone.value for phone in self._phones]

    @phones.setter
    def phones(self, phones: List[str]) -> None:
        self._phones = [PhoneField(phone) for phone in phones]

    @property
    def birthday(self) -> Optional[datetime.date]:
        return self._birthday.value if self._birthday else None

    @birthday.setter
    def birthday(self, birthday: str) -> None:
        self._birthday = DateField(birthday)

    @property
    def address(self) -> Optional[str]:
        return str(self._address)

    @address.setter
    def address(self, address: str) -> None:
        self._address = AddressField(address)

    @property
    def email(self) -> Optional[str]:
        return str(self._email)

    @email.setter
    def email(self, email: str) -> None:
        self._email = EmailField(email)

    @property
    def notes(self) -> List[NoteField]:
        return self._notes

    @notes.setter
    def notes(self, notes: List[Tuple[str, List[str]]]) -> None:
        self._notes = [NoteField(note, tags) for note, tags in notes]

    def add_phone(self, phone_number: str) -> None:
        self._phones.append(PhoneField(phone_number))

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        self.remove_phone(old_phone_number)
        self.add_phone(new_phone_number)

    def remove_phone(self, phone_number: str) -> None:
        for index, p in enumerate(self._phones):
            if p.value == phone_number:
                del self._phones[index]
                return

    def has_phone(self, phone_number: str) -> bool:
        for phone in self._phones:
            if phone.value == phone_number:
                return True
        return False

    def add_note(self, note: str, tags: List[str] = None) -> None:
        new_note = NoteField(note)
        if tags:
            for tag in tags:
                new_note.add_tag(tag)
        self._notes.append(new_note)

    def edit_note(self, index_to_change: int, new_note: str, new_tags: List[str] = None) -> None:
        if 0 <= index_to_change < len(self._notes):
            updated_note = NoteField(new_note)
            if new_tags:
                for tag in new_tags:
                    updated_note.add_tag(tag)
            self._notes[index_to_change] = updated_note

    def remove_note(self, index_to_remove: int) -> None:
        del self._notes[index_to_remove - 1]

    def has_note(self, note_to_search: str) -> bool:
        for note in self._notes:
            if note_to_search in note.value:
                return True
        return False

    def add_tag_to_note(self, index: int, tag: str) -> None:
        if 0 <= index < len(self._notes):
            self._notes[index].add_tag(tag)

    def remove_tag_from_note(self, index: int, tag: str) -> None:
        if 0 <= index < len(self._notes):
            self._notes[index].remove_tag(tag)

    def search_notes_by_tag(self, tag: str) -> List[Tuple[int, str, List[str]]]:
        return [(i, note.value, note.tags) for i, note in enumerate(self._notes) if tag in note.tags]

    def sort_notes_by_tags(self) -> List[Tuple[int, str, List[str]]]:
        return sorted([(i, note.value, note.tags) for i, note in enumerate(self._notes)],
                      key=lambda x: len(x[2]), reverse=True)

    def dto(self) -> CustomerDTO:
        return CustomerDTO(
            id=str(self._id) if self._id.value else None,
            name=self._name.value,
            phones=[str(phone) for phone in self._phones],
            birthday=str(self._birthday) if self._birthday.value else None,
            address=self._address.value,
            email=self._email.value,
            notes=[str(note) for note in self._notes],
        )

    def __str__(self) -> str:
        notes_str = '\n'.join([f"{i + 1} - {note.value} (Tags: {', '.join(note.tags)});"
                               for i, note in enumerate(self._notes)])
        return (f"Customer name: {str(self.name)}, phones: {'; '.join(self.phones)}\n{notes_str}")
