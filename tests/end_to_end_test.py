from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_end_to_end_real_adapters() -> None:
    # Step 1: Simulate file upload
    file_content = b"Sample content for the real tests"
    response = client.post(
        "/save-document/",
        files={"file": ("real_test_document.txt", file_content, "text/plain")},
    )
    assert response.status_code == 201
    assert response.json() == {"status": "Document saved successfully"}

    # Step 2: Ask a question using the real adapters
    # query = {"query": "What is the document about?"}
    # response = client.get("/generate-answer/", params=query)
    # assert response.status_code == 201
    # print(f"Generated Answer: {response.json()}")
    # assert "answer" in response.json()


def test_user_registration_and_login_real_adapters() -> None:
    # Step 1: Register a new user with real MongoDB connection
    response = client.post(
        "/register/",
        params={"username": "realuser", "password": "realpassword", "rol": "user"},
    )
    assert response.status_code == 201
    assert response.json() == {"status": "User created successfully"}

    # Step 2: Log in with the registered user
    response = client.get(
        "/login/", params={"username": "realuser", "password": "realpassword"}
    )
    assert response.status_code == 201
    assert response.json() == {"status": "User logged in successfully"}
