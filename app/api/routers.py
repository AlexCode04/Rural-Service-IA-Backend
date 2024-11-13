from fastapi import APIRouter, Depends, UploadFile, File
from app import usecases
from app.api import dependencies

rag_router = APIRouter()


def depends() -> Depends:
    return Depends(dependencies.RAGServiceSingleton.get_instance)


@rag_router.post("/save-document/", status_code=201)
def save_document(
    file: UploadFile = File(...),
    rag_service: usecases.RAGService = depends(),
) -> dict:
    rag_service.save_document(file)
    return {"status": "Document saved successfully"}


@rag_router.get("/generate-answer/", status_code=201)
def generate_answer(
    query: str,
    rag_service: usecases.RAGService = depends(),
) -> str:
    return rag_service.generate_answer(query)


@rag_router.post("/register/", status_code=201)
def sing_up(
    email: str,
    password: str,
    rag_service: usecases.RAGService = depends(),
) -> dict:
    response = rag_service.sing_up(email, password)
    return response


@rag_router.get("/login/", status_code=201)
def get_user(
    email: str,
    password: str,
    rag_service: usecases.RAGService = depends(),
) -> dict:
    user = rag_service.get_user(email, password)
    if user.email == "":
        return {"status": "User not found"}
    return {"status": "User logged in successfully"}


@rag_router.post("/change-role/", status_code=201)
def change_role(
    email: str,
    new_role: str,
    rag_service: usecases.RAGService = depends(),
) -> dict:
    response = rag_service.change_role(email, new_role)
    return response


@rag_router.get("/get-all-users/", status_code=200)
def get_all_users(
    rag_service: usecases.RAGService = depends(),
) -> dict:
    users = rag_service.get_all_users()
    return {"users": users}
