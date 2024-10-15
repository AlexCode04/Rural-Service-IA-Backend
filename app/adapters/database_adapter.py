from bson import ObjectId
from app.core import ports, models
from pymongo import MongoClient
from app.core.models import Document


class MongoDbAdapter(ports.DatabasePort):
    def __init__(self, url: str) -> None:
        self.client = MongoClient(url)
        #nombre de la base de datos
        self.db = self.client["rag_db"]
        #nombre de las colecciones
        self.users = self.db["users"]
        self.documents = self.db["documents"]

    def save_user(self, user: models.User) -> None:
        self.users.insert_one({ "user_id": user.user_id,"username": user.username, "password": user.password, "rol": user.rol})

    def get_user(self, username: str, password: str) -> models.User:
        user = self.users.find_one({"username": username, "password": password})
        documents = self.documents.find({"user_id": user["user_id"]})
        if user:
            return models.User(username=user["username"], password=user["password"], rol=user["rol"], documents=documents)
        return models.User(username="", password="")

    def save_document(self, document: models.Document) -> None:
        self.documents.insert_one({"user_id": document.user_id,"document_id": document.document_id, "nombre": document.nombre, "ruta": document.ruta})

    def get_document(self, document_id: str) -> Document | None:
        document = self.documents.find_one({"document_id": document_id})
        if document:
            return models.Document(document_id=document["document_id"], nombre=document["nombre"], ruta=document["ruta"])
        return None

    def get_documents_by_user_id(self, user_id: str) -> list[Document]:
        documents = self.documents.find({"user_id": user_id}, {"_id": 0})  # Excluir el campo _id de la respuesta
        docs_list = []
        for document in documents:
            docs_list.append(
                models.Document(
                    document_id=document["document_id"],
                    nombre=document["nombre"],
                    ruta=document["ruta"],
                    user_id=document["user_id"]
                )
            )
        return docs_list
