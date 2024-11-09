from unittest.mock import Mock, patch
from app.core.models import Document, User
from app.usecases import RAGService
from app.core import ports
import pytest

# This test is using the Mock class from the unittest.mock module to create mock objects for the database adapter, document repository, and OpenAI adapter.


@pytest.fixture
def mock_db_adapter() -> Mock:
    return Mock(spec=ports.DatabasePort)


@pytest.fixture
def mock_document_repo() -> Mock:
    return Mock(spec=ports.DocumentRepositoryPort)


@pytest.fixture
def mock_openai_adapter() -> Mock:
    return Mock(spec=ports.LlmPort)


@pytest.fixture
def rag_service(
    mock_db_adapter: Mock, mock_document_repo: Mock, mock_openai_adapter: Mock
) -> RAGService:
    return RAGService(
        db=mock_db_adapter,
        document_repo=mock_document_repo,
        openai_adapter=mock_openai_adapter,
    )


def test_save_document_should_save_file_and_document(
    rag_service: RAGService, mock_document_repo: Mock, mock_openai_adapter: Mock
) -> None:
    # Arrange
    file = Mock()
    file.filename = "test_file.txt"
    file.file.read.return_value = b"This is a tests file"

    # Act
    with patch("os.makedirs"), patch("builtins.open", mock_open=True):
        rag_service.save_document(file)

    # Assert
    mock_document_repo.save_document.assert_called_once()


def test_generate_answer_should_return_generated_text(
    rag_service: RAGService, mock_document_repo: Mock, mock_openai_adapter: Mock
) -> None:
    # Arrange
    query = "What is the document about?"
    mock_document_repo.get_documents.return_value = [
        Document(document_id="doc1", content="Document content 1"),
        Document(document_id="doc2", content="Document content 2"),
    ]
    mock_openai_adapter.generate_text.return_value = "Generated response"

    # Act
    result = rag_service.generate_answer(query)

    # Assert
    mock_document_repo.get_documents.assert_called_once_with(query, mock_openai_adapter)
    mock_openai_adapter.generate_text.assert_called_once_with(
        prompt=query, retrieval_context="Document content 1 Document content 2"
    )
    assert result == "Generated response"


def test_sing_up_should_save_user(
    rag_service: RAGService, mock_db_adapter: Mock
) -> None:
    # Arrange
    email = "testuser"
    password = "password"

    # Act
    rag_service.sing_up(email, password)

    # Assert
    mock_db_adapter.save_user.assert_called_once()


def test_get_user_should_return_user(
    rag_service: RAGService, mock_db_adapter: Mock
) -> None:
    # Arrange
    email = "testuser"
    password = "password"
    mock_db_adapter.get_user.return_value = User(
        email=email, password=password, rol="admin"
    )

    # Act
    result = rag_service.get_user(email, password)

    # Assert
    mock_db_adapter.get_user.assert_called_once_with(email, password)
    assert result.email == email
    assert result.password == password
    assert result.rol == "admin"


def test_change_role_should_update_user_role(
    rag_service: RAGService, mock_db_adapter: Mock
) -> None:
    # Arrange
    email = "testuser"
    new_role = "admin"

    # Configuración del mock para devolver el usuario existente
    mock_db_adapter.get_user_by_email.return_value = User(
        email=email, password="password", rol="user"
    )
    mock_db_adapter.update_user_with_new_role.return_value = {
        "status": "User updated successfully"
    }

    # Act
    result = rag_service.change_role(email, new_role)

    # Assert
    mock_db_adapter.get_user_by_email.assert_called_once_with(email)
    mock_db_adapter.update_user_with_new_role.assert_called_once()
    assert result == {"status": "Role changed successfully"}


def test_change_role_should_return_error_when_user_not_found(
    rag_service: RAGService, mock_db_adapter: Mock
) -> None:
    # Arrange
    email = "testuser"
    new_role = "admin"

    # Configuración del mock para devolver None cuando se busque el usuario
    mock_db_adapter.get_user_by_email.return_value = None

    # Act
    result = rag_service.change_role(email, new_role)

    # Assert
    mock_db_adapter.get_user_by_email.assert_called_once_with(email)
    mock_db_adapter.update_user_with_new_role.assert_not_called()
    assert result == {"status": "User not found"}


def test_get_all_users_should_return_all_users(
    rag_service: RAGService, mock_db_adapter: Mock
) -> None:
    # Arrange
    mock_db_adapter.get_all_users.return_value = [
        User(email="user1", password="password1", rol="admin"),
        User(email="user2", password="password2", rol="user"),
    ]

    # Act
    result = rag_service.get_all_users()

    # Assert
    mock_db_adapter.get_all_users.assert_called_once()
    assert len(result) == 2
    assert result[0].email == "user1"
    assert result[0].password == "password1"
    assert result[0].rol == "admin"
    assert result[1].email == "user2"
    assert result[1].password == "password2"
    assert result[1].rol == "user"
