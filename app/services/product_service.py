from google.api_core.exceptions import AlreadyExists

from app.models.product import ProductCreateRequest, ProductResponse, ProductUpdateRequest
from app.repositories.product_repository import ProductRepository


def derive_status(quantity: int) -> str:
    return "in_stock" if quantity > 0 else "out_of_stock"


class ProductAlreadyExistsError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def create_product(self, payload: ProductCreateRequest) -> ProductResponse:
        try:
            created = self._repository.create(
                product_name=payload.product_name,
                quantity=payload.quantity,
                status=derive_status(payload.quantity),
                product_id=payload.product_id,
            )
        except AlreadyExists as exc:
            raise ProductAlreadyExistsError from exc
        return ProductResponse(**created)

    def list_products(self) -> list[ProductResponse]:
        return [ProductResponse(**item) for item in self._repository.list_all()]

    def get_product(self, product_id: str) -> ProductResponse:
        product = self._repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError
        return ProductResponse(**product)

    def update_product(self, product_id: str, payload: ProductUpdateRequest) -> ProductResponse:
        try:
            updated = self._repository.update(
                product_id=product_id,
                product_name=payload.product_name,
                quantity=payload.quantity,
                status=derive_status(payload.quantity),
            )
        except KeyError as exc:
            raise ProductNotFoundError from exc
        return ProductResponse(**updated)

    def delete_product(self, product_id: str) -> None:
        deleted = self._repository.delete(product_id)
        if not deleted:
            raise ProductNotFoundError
