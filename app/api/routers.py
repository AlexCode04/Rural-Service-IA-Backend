import pydantic
from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel
from app import usecases
from app.api import dependencies

rag_router = APIRouter()

@rag_router.post("/save-document/", status_code=201)
def save_document(user_id: str, file: UploadFile = File(...),
                  rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    # Guardar la información del archivo en MongoDB
    rag_service.save_document(file, user_id)
    return {"status": "Document saved successfully"}

@rag_router.get("/get-document/")
def get_document(document_id: str,
                 rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    document = rag_service.get_document(document_id)
    if document:
        return document
    return {"status": "Document not found"}

@rag_router.get("/get-vectors/", status_code=201)
def get_vectors(rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    return rag_service.get_vectors()

@rag_router.get("/generate-answer/", status_code=201)
def generate_answer(query: str,
                    rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    return rag_service.generate_answer(query)

@rag_router.post("/sing-up/", status_code=201)
def sing_up(username: str, password: str, rol: str,
            rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    rag_service.sing_up(username, password, rol)
    return {"status": "User created successfully"}

@rag_router.get("/login/", status_code=201)
def get_user(username: str, password: str,
            rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    user = rag_service.get_user(username, password)
    if user.username == "":
        return {"status": "User not found"}
    return {"status": "User logged in successfully"}

@rag_router.get("/get-documents-by-user-id/", status_code=201)
def get_documents_by_user_id(user_id: str,
            rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance)):
    documents = rag_service.get_documents_by_user_id(user_id)
    return documents