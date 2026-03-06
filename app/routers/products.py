from fastapi import APIRouter, Depends, HTTPException, status

from app.models.auth import AuthMessageResponse
from app.models.product import ProductCreateRequest, ProductResponse, ProductUpdateRequest
from app.services.container import get_product_service
from app.services.product_service import ProductAlreadyExistsError, ProductNotFoundError, ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreateRequest,
    product_service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    try:
        return product_service.create_product(payload)
    except ProductAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail="product already exists") from exc


@router.get("", response_model=list[ProductResponse])
def list_products(product_service: ProductService = Depends(get_product_service)) -> list[ProductResponse]:
    return product_service.list_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, product_service: ProductService = Depends(get_product_service)) -> ProductResponse:
    try:
        return product_service.get_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="product not found") from exc


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    payload: ProductUpdateRequest,
    product_service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    try:
        return product_service.update_product(product_id, payload)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="product not found") from exc


@router.delete("/{product_id}", response_model=AuthMessageResponse)
def delete_product(product_id: str, product_service: ProductService = Depends(get_product_service)) -> AuthMessageResponse:
    try:
        product_service.delete_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail="product not found") from exc
    return AuthMessageResponse(message="product deleted")
