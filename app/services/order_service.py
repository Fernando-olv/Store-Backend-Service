from datetime import UTC, datetime

from google.cloud import firestore

from app.models.order import OrderCreateRequest, OrderPlacedResponse, OrderResponse
from app.services.product_service import derive_status


class ProductNotFoundError(Exception):
    pass


class NoStockError(Exception):
    pass


class OrderNotFoundError(Exception):
    pass


class OrderAccessDeniedError(Exception):
    pass


class OrderService:
    def __init__(self, client: firestore.Client) -> None:
        self._client = client
        self._products = client.collection("products")
        self._orders = client.collection("orders")

    def place_order(self, buyer_email: str, payload: OrderCreateRequest) -> OrderPlacedResponse:
        transaction = self._client.transaction()
        product_ref = self._products.document(payload.product_id)
        order_ref = self._orders.document()

        @firestore.transactional
        def _run(txn: firestore.Transaction) -> None:
            product_snapshot = product_ref.get(transaction=txn)
            if not product_snapshot.exists:
                raise ProductNotFoundError

            product = product_snapshot.to_dict() or {}
            available_qty = int(product.get("quantity", 0))
            if payload.quantity > available_qty:
                raise NoStockError

            new_qty = available_qty - payload.quantity
            txn.update(
                product_ref,
                {
                    "quantity": new_qty,
                    "status": derive_status(new_qty),
                    "updated_at": datetime.now(UTC),
                },
            )

            txn.set(
                order_ref,
                {
                    "order_id": order_ref.id,
                    "created_at": datetime.now(UTC),
                    "buyer_email": buyer_email,
                    "product_id": payload.product_id,
                    "quantity": payload.quantity,
                },
            )

        _run(transaction)

        created = order_ref.get().to_dict() or {}
        return OrderPlacedResponse(message="order_placed", order=OrderResponse(**created))

    def list_orders(self, buyer_email: str) -> list[OrderResponse]:
        query = self._orders.where(filter=firestore.FieldFilter("buyer_email", "==", buyer_email))
        return [OrderResponse(**doc.to_dict()) for doc in query.stream()]

    def get_order(self, buyer_email: str, order_id: str) -> OrderResponse:
        snapshot = self._orders.document(order_id).get()
        if not snapshot.exists:
            raise OrderNotFoundError

        data = snapshot.to_dict() or {}
        if data.get("buyer_email") != buyer_email:
            raise OrderAccessDeniedError
        return OrderResponse(**data)
