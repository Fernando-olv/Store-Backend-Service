from datetime import datetime

from pydantic import BaseModel, Field


class OrderCreateRequest(BaseModel):
    product_id: str = Field(min_length=1, max_length=128)
    quantity: int = Field(gt=0)


class OrderResponse(BaseModel):
    order_id: str
    created_at: datetime | None = None
    buyer_email: str
    product_id: str
    quantity: int


class OrderPlacedResponse(BaseModel):
    message: str
    order: OrderResponse
