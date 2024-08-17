from typing import Optional

from src.modules.dto.booking_dto import BookingDTO
from src.modules.models.fields.datetime_field import DatetimeField
from src.modules.models.fields.id_field import IDField


class Booking:
    """Customer booking model"""

    def __init__(self, dto: BookingDTO = None):
        if not dto:
            dto = BookingDTO()

        self._id = IDField(dto.id)
        self._customer_id: Optional[IDField] = IDField(dto.customer_id) if dto.customer_id else None
        self._date: Optional[DatetimeField] = DatetimeField(dto.date, validate=False)

    @property
    def id(self) -> str:
        return str(self._id)

    @property
    def customer_id(self) -> Optional[str]:
        return str(self._customer_id) if self._customer_id else None

    @customer_id.setter
    def customer_id(self, new_customer_id: str) -> None:
        self._customer_id = IDField(new_customer_id)

    @property
    def date(self) -> Optional[str]:
        return str(self._date) if self._date.value else None

    @date.setter
    def date(self, new_date: str) -> None:
        self._date = DatetimeField(new_date)

    def dto(self) -> BookingDTO:
        return BookingDTO(
            id=str(self._id.value),
            customer_id=str(self._customer_id.value),
            date=str(self._date) if self._date.value else None
        )

    def __str__(self) -> str:
        return f": Booking for customer {self.customer_id} on {self.date}"
