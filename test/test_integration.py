import pytest
from unittest.mock import Mock
from pymongo import MongoClient
from app.core import ports
from app.usecases import RAGService
from app.adapters.database_adapter import MongoDbAdapter


@pytest.fixture
def mock_document_repo() -> Mock:
    return Mock(spec=ports.DocumentRepositoryPort)


@pytest.fixture
def mock_openai_adapter() -> Mock:
    return Mock(spec=ports.LlmPort)


@pytest.fixture(scope="function")
def mongo_db() -> MongoClient:
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client["test_rag_db"]
    # Limpiar la colección antes de cada prueba
    db.users.delete_many({})
    yield db
    client.drop_database("test_rag_db")
    # Limpiar la base de datos al finalizar


@pytest.fixture
def mongo_adapter(mongo_db: MongoClient) -> MongoDbAdapter:
    # Crear una instancia del adaptador MongoDbAdapter con la base de datos de prueba
    return MongoDbAdapter("mongodb://127.0.0.1:27017")  # Pasar la URL correcta


@pytest.fixture
def rag_service(
    mongo_adapter: MongoDbAdapter, mock_document_repo: Mock, mock_openai_adapter: Mock
) -> RAGService:
    # Configurar RAGService con el adaptador MongoDB y los mocks necesarios
    return RAGService(
        db=mongo_adapter,
        document_repo=mock_document_repo,
        openai_adapter=mock_openai_adapter,
    )


def test_log_in_should_return_user(
    rag_service: RAGService, mongo_db: MongoClient
) -> None:
    # Arrange
    username = "testuser"
    password = "password"
    rol = "admin"

    # Act
    mongo_db["users"].insert_one(
        {"username": username, "password": password, "rol": rol}
    )
    user = rag_service.get_user(username, password)

    # Assert
    assert user is not None
    assert user.username == username
    assert user.password == password
    assert user.rol == rol


def test_get_user_not_found(rag_service: RAGService) -> None:
    # Act
    user = rag_service.get_user("nonexistent_user", "wrong_password")
    # Assert
    assert user is None


# def test_sing_up_should_save_user(rag_service: RAGService, mongo_db: MongoClient, mongo_adapter: MongoDbAdapter) -> None:
#     # Datos de prueba
#     username = "testuser"
#     password = "password"
#     rol = "admin"
#
#     user = User(username=username, password=password, rol=rol)
#
#     # Limpiar duplicados
#     mongo_db["users"].delete_many({"username": username})
#     mongo_adapter.save_user(user)
#     # rag_service.sing_up(username, password, rol)
#
#
#     # Verificar si el usuario fue guardado en MongoDB
#     user = mongo_db["users"].find_one({"username": username})
#     print(user)
#     assert user is not None
#     assert user["username"] == username
#     assert user["password"] == password
#     assert user["rol"] == rol
