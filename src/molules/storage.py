""""Module for storing contacts and notes in a file"""


import csv
from typing import List, Type, TypeVar, Generic

D = TypeVar('D')


class Storage(Generic[D]):
    def __init__(self, dto_cls: Type[D], filename: str):
        self.dto_cls = dto_cls
        self.filename = filename

    def save(self, dtos: List[D]) -> None:
        """Save a list of DTOs to a CSV file."""
        if not dtos:
            return

        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self._get_fieldnames())
            writer.writeheader()
            for dto in dtos:
                writer.writerow(dto.to_dict())

    def load(self) -> List[D]:
        """Load a list of DTOs from a CSV file."""
        dtos = []
        try:
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.DictReader(file, fieldnames=self._get_fieldnames())
                next(reader, None)
                for row in reader:
                    dto = self.dto_cls()
                    dtos.append(dto.from_dict(row))
        except FileNotFoundError:
            return dtos
        return dtos

    def clear(self) -> None:
        """Delete the file."""
        try:
            import os
            os.remove(self.filename)
        except FileNotFoundError:
            pass

    def _get_fieldnames(self) -> List[str]:
        """Get the fieldnames for the CSV. This assumes all DTOs have the same fields."""
        dummy_dto = self.dto_cls()
        return dummy_dto.get_fields()
