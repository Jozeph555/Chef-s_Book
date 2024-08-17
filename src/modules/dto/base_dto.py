from typing import Optional

from pydantic import BaseModel


class BaseDTO(BaseModel):
    id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'BaseDTO':
        return cls(
            id=data.get('id'),
        )

    def to_dict(self) -> dict:
        return {'id': self.id, }

    @classmethod
    def get_fields(cls):
        return list(cls.__annotations__.keys())

    def empty_string_to_none(value):
        return value if value != '' else None
