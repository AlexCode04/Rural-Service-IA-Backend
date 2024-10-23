from app.core import ports, models
from pymongo import MongoClient


class MongoDbAdapter(ports.DatabasePort):
    def __init__(self, url: str) -> None:
        self.client = MongoClient(url)
        # Nombre de la base de datos
        self.db = self.client["rag_db"]
        # Nombre de las colecciones
        self.users = self.db["users"]
        self.documents = self.db["documents"]

    def save_user(self, user: models.User) -> None:
        self.users.insert_one({
            "user_id": user.user_id,
            "username": user.username,
            "password": user.password,
            "rol": user.rol
        })

    def get_user(
        self, username: str, _pass: str
    ) -> models.User:
        user = self.users.find_one({"username": username, "password": _pass})
        if user:
            return models.User(
                username=user["username"],
                password=user["password"],
                rol=user["rol"]
            )
        return models.User(username="", password="", rol="")
