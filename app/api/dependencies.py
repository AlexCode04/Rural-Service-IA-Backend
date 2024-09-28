from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.chromadb_adapter import ChromaDBAdapter
from app.adapters.database_adapter import MongoDbAdapter
from app import usecases
from app import configurations


class RAGServiceSingleton:
    _instance = None

    @classmethod
    def get_instance(cls) -> usecases.RAGService:
        if cls._instance is None:

            database_adapter = MongoDbAdapter(url="mongodb://127.0.0.1:27017")
            cls._instance = usecases.RAGService(db=database_adapter)

        return cls._instance
