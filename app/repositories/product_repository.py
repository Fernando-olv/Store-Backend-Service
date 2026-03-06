import uuid
from datetime import datetime, timezone

from google.cloud import firestore


class ProductRepository:
    def __init__(self, client: firestore.Client) -> None:
        self._collection = client.collection("products")

    def create(self, product_name: str, quantity: int, status: str, product_id: str | None = None) -> dict:
        resolved_id = product_id or str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        payload = {
            "product_id": resolved_id,
            "product_name": product_name,
            "quantity": quantity,
            "status": status,
            "created_at": now,
            "updated_at": now,
        }
        self._collection.document(resolved_id).create(payload)
        return payload

    def list_all(self) -> list[dict]:
        docs = self._collection.stream()
        return [doc.to_dict() for doc in docs]

    def get_by_id(self, product_id: str) -> dict | None:
        doc = self._collection.document(product_id).get()
        if not doc.exists:
            return None
        return doc.to_dict()

    def update(self, product_id: str, product_name: str, quantity: int, status: str) -> dict:
        doc_ref = self._collection.document(product_id)
        if not doc_ref.get().exists:
            raise KeyError(product_id)
        updates = {
            "product_name": product_name,
            "quantity": quantity,
            "status": status,
            "updated_at": datetime.now(timezone.utc),
        }
        doc_ref.update(updates)
        updated = doc_ref.get().to_dict() or {}
        return updated

    def delete(self, product_id: str) -> bool:
        doc_ref = self._collection.document(product_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True
