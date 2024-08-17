from typing import List, Optional

from src.modules.dto.base_dto import BaseDTO


class CustomerDTO(BaseDTO):
    id: Optional[str] = None
    name: Optional[str] = None
    birthday: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phones: List[str] = []
    notes: List[str] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, data: dict) -> 'CustomerDTO':
        def empty_string_to_none(value):
            return value if value != '' else None

        return cls(
            id=empty_string_to_none(data.get('id')),
            name=empty_string_to_none(data.get('name')),
            phones=[phone for phone in data.get('phones', '').split(';') if phone] if data.get('phones') else [],
            notes=[note for note in data.get('notes', '').split(';') if note] if data.get('notes') else [],
            birthday=empty_string_to_none(data.get('birthday')),
            address=empty_string_to_none(data.get('address')),
            email=empty_string_to_none(data.get('email'))
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name or '',
            'phones': ';'.join(self.phones) if self.phones else '',
            'notes': ';'.join(self.notes) if self.notes else '',
            'birthday': self.birthday or '',
            'address': self.address or '',
            'email': self.email or ''
        }
