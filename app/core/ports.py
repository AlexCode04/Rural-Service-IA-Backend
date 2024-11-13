from abc import ABC, abstractmethod
from typing import List, Optional  # Importamos Optional para parámetros opcionales
from app.core import models


class DocumentRepositoryPort(ABC):
    @abstractmethod
    def save_document(
        self, doc: models.Document, text: str, openai_client: "LlmPort"
    ) -> None:
        pass

    @abstractmethod
    def get_documents(
        self, query: str, openai_client: "LlmPort", n_results: Optional[int] = None
    ) -> List[models.Document]:
        pass


class LlmPort(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, retrieval_context: str) -> str:
        pass

    @abstractmethod
    def create_embeddings(self, text: str) -> list[float]:
        pass


class DatabasePort(ABC):
    @abstractmethod
    def save_user(self, user: models.User) -> dict:
        pass

    @abstractmethod
    def get_user(self, username: str, password: str) -> Optional[models.User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[models.User]:
        pass

    @abstractmethod
    def update_user_with_new_role(self, user: models.User) -> dict:
        pass

    @abstractmethod
    def get_all_users(self) -> List[models.User]:
        pass
