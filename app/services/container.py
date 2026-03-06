from functools import lru_cache

from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.firestore_client import get_firestore_client
from app.services.jwt_service import JWTService
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.services.settings import get_settings


@lru_cache(maxsize=1)
def get_jwt_service() -> JWTService:
    settings = get_settings()
    return JWTService(
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        expiration_minutes=settings.jwt_expiration_minutes,
    )


@lru_cache(maxsize=1)
def get_auth_service() -> AuthService:
    client = get_firestore_client()
    return AuthService(UserRepository(client), get_jwt_service())


@lru_cache(maxsize=1)
def get_product_service() -> ProductService:
    client = get_firestore_client()
    return ProductService(ProductRepository(client))


@lru_cache(maxsize=1)
def get_order_service() -> OrderService:
    return OrderService(get_firestore_client())
