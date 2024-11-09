from typing import Optional
from app.core import ports, models
from pymongo import MongoClient


class MongoDbAdapter(ports.DatabasePort):
    def __init__(self, url: str, db_name: str) -> None:
        self.client = MongoClient(url)
        # Nombre de la base de datos
        self.db = self.client[db_name]
        # Nombre de las colecciones
        self.users = self.db["users"]

    def save_user(self, user: models.User) -> dict:
        user_clone = self.users.find_one({"email": user.email})

        if user_clone:
            return {"status": "User already exists"}

        self.users.insert_one(
            {
                "user_id": user.user_id,
                "email": user.email,
                "password": user.password,
                "rol": user.rol,
            }
        )

        return {"status": "User created successfully"}

    def get_user(self, email: str, _pass: str) -> Optional[models.User]:
        user = self.users.find_one({"email": email, "password": _pass})
        if user:
            return models.User(
                email=user["email"], password=user["password"], rol=user["rol"]
            )
        return None

    def get_user_by_email(self, email: str) -> Optional[models.User]:
        user = self.users.find_one({"email": email})
        if user:
            return models.User(
                email=user["email"], password=user["password"], rol=user["rol"]
            )
        return None

    def update_user_with_new_role(self, user: models.User) -> dict:
        self.users.update_one(
            {"email": user.email},
            {"$set": {"rol": user.rol}},
        )

        return {"status": "User updated successfully"}

    def get_all_users(self) -> list[models.User]:
        users = self.users.find()
        return [
            models.User(email=user["email"], password=user["password"], rol=user["rol"])
            for user in users
        ]
