from fastapi import APIRouter, Depends, HTTPException, status

from app.models.order import OrderCreateRequest, OrderPlacedResponse, OrderResponse
from app.services.auth_dependencies import get_current_user_email
from app.services.container import get_order_service
from app.services.order_service import (
    NoStockError,
    OrderAccessDeniedError,
    OrderNotFoundError,
    OrderService,
    ProductNotFoundError,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderPlacedResponse, status_code=status.HTTP_201_CREATED)
def place_order(
    payload: OrderCreateRequest,
    buyer_email: str = Depends(get_current_user_email),
    order_service: OrderService = Depends(get_order_service),
) -> OrderPlacedResponse:
    try:
        return order_service.place_order(buyer_email, payload)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="product not found") from exc
    except NoStockError as exc:
        raise HTTPException(status_code=409, detail="no_stock") from exc


@router.get("", response_model=list[OrderResponse])
def list_orders(
    buyer_email: str = Depends(get_current_user_email),
    order_service: OrderService = Depends(get_order_service),
) -> list[OrderResponse]:
    return order_service.list_orders(buyer_email)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    buyer_email: str = Depends(get_current_user_email),
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    try:
        return order_service.get_order(buyer_email, order_id)
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=404, detail="order not found") from exc
    except OrderAccessDeniedError as exc:
        raise HTTPException(status_code=403, detail="forbidden") from exc
