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


@rag_router.get("/get-vectors/", status_code=200)
def get_vectors(
    rag_service: usecases.RAGService = depends(),
) -> dict:  # Cambiado a dict para que FastAPI lo maneje sin problemas
    vectors = rag_service.get_vectors()
    # Convierte `vectors` a un formato JSON serializable, si es necesario
    return {"vectors": vectors}


@rag_router.get("/generate-answer/", status_code=201)
def generate_answer(
    query: str,
    rag_service: usecases.RAGService = depends(),
) -> str:
    return rag_service.generate_answer(query)


@rag_router.post("/register/", status_code=201)
def sing_up(
    username: str,
    password: str,
    rol: str,
    rag_service: usecases.RAGService = depends(),
) -> dict:
    rag_service.sing_up(username, password, rol)
    return {"status": "User created successfully"}


@rag_router.get("/login/", status_code=201)
def get_user(
    username: str,
    password: str,
    rag_service: usecases.RAGService = depends(),
) -> dict:
    user = rag_service.get_user(username, password)
    if user.username == "":
        return {"status": "User not found"}
    return {"status": "User logged in successfully"}
