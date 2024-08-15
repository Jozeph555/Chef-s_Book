from typing import List, Optional

from src.modules.dto.base_dto import BaseDTO


class BookingDTO(BaseDTO):
    id: Optional[str] = None
    customer_id: Optional[str] = None
    date: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, data: dict) -> 'BookingDTO':
        return cls(
            id=data.get('id'),
            customer_id=data.get('customer_id'),
            date=data.get('date')
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'customer_id': self.customer_id or '',
            'date': self.date or ''
        }
