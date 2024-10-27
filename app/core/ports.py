from abc import ABC, abstractmethod
from typing import List, Optional  # Importamos Optional para parámetros opcionales
from app.core import models
from chromadb.api.types import GetResult


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

    @abstractmethod
    def get_vectors(
        self,
    ) -> GetResult:  # Anotación para lista de listas de floats
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
    def save_user(self, user: models.User) -> None:
        pass

    @abstractmethod
    def get_user(self, username: str, password: str) -> Optional[models.User]:
        pass
