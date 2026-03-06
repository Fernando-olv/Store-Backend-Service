from datetime import datetime, timezone

from google.cloud import firestore


class UserRepository:
    def __init__(self, client: firestore.Client) -> None:
        self._collection = client.collection("users")

    def get_by_email(self, email: str) -> dict | None:
        doc = self._collection.document(email).get()
        if not doc.exists:
            return None
        data = doc.to_dict() or {}
        data["email"] = email
        return data

    def create_user(self, email: str, password_hash: str) -> dict:
        payload = {
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.now(timezone.utc),
        }
        self._collection.document(email).set(payload)
        return payload
