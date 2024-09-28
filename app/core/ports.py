from abc import ABC, abstractmethod
from typing import List
from app.core import models





class DatabasePort(ABC):
    @abstractmethod
    def save_user(self, username: str, password: str) -> None:
        pass

    @abstractmethod
    def get_user(self, username: str, password: str) -> models.User:
        pass

    @abstractmethod
    def save_document(self, document: models.Document) -> None:
        pass

    @abstractmethod
    def get_document(self, document_id: str) -> models.Document | None:
        pass


