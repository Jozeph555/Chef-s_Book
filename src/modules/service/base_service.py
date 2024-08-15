from collections import UserList
from typing import Type, TypeVar, Generic, List, Optional

from src.modules.storage import Storage

D = TypeVar('D')
M = TypeVar('M')


class BaseService(UserList, Generic[D, M]):
    """Base class to manage model instances"""

    def __init__(self, dto_cls: Type[D], model_cls: Type[M], data_file: str):
        super().__init__()

        self.storage = Storage(dto_cls, data_file)
        self.data: List[M] = [model_cls(dto) for dto in self.storage.load()]

    def add(self, record: M) -> None:
        self.data.append(record)

    def delete(self, record_id: str) -> None:
        self.data = [record for record in self.data if record.id != record_id]

    def find(self, record_id: str) -> Optional[M]:
        for record in self.data:
            if record.id == record_id:
                return record
        return None

    def save(self) -> None:
        self.storage.save([record.dto() for record in self.data])

    def clear(self) -> None:
        self.data.clear()
        self.storage.clear()
