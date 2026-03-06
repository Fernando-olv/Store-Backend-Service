from google.cloud import firestore


class OrderRepository:
    def __init__(self, client: firestore.Client) -> None:
        self._collection = client.collection("orders")

    def get_by_id(self, order_id: str) -> dict | None:
        doc = self._collection.document(order_id).get()
        if not doc.exists:
            return None
        return doc.to_dict()

    def list_by_buyer_email(self, buyer_email: str) -> list[dict]:
        query = self._collection.where(filter=firestore.FieldFilter("buyer_email", "==", buyer_email))
        return [doc.to_dict() for doc in query.stream()]
