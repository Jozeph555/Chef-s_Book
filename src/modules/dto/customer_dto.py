from typing import List, Optional

from src.modules.dto.base_dto import BaseDTO


class CustomerDTO(BaseDTO):
    name: Optional[str] = None
    phones: List[str] = []
    birthday: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, data: dict) -> 'CustomerDTO':
        return cls(
            id=data.get('id', None),
            name=data.get('name', None),
            phones=data.get('phones').split(';') if data.get('phones') else None,
            birthday=data.get('birthday', None),
            address=data.get('address', None),
            email=data.get('email', None)
        )

    def to_dict(self) -> dict:
        print('EMAIL', self.email or '')
        return {
            'id': self.id,
            'name': self.name or '',
            'phones': ';'.join(self.phones) if self.phones else '',
            'birthday': self.birthday or '',
            'address': self.address or '',
            'email': self.email or ''
        }

    @classmethod
    def get_fields(cls):
        fields = set(cls.__annotations__.keys())
        for base in cls.__bases__:
            fields.update(base.__annotations__.keys())
        return list(fields)
