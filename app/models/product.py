from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ProductStatus = Literal["in_stock", "out_of_stock"]


class ProductCreateRequest(BaseModel):
    product_id: str | None = Field(default=None, min_length=1, max_length=128)
    product_name: str = Field(min_length=1, max_length=255)
    quantity: int = Field(ge=0)


class ProductUpdateRequest(BaseModel):
    product_name: str = Field(min_length=1, max_length=255)
    quantity: int = Field(ge=0)


class ProductResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    status: ProductStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None
