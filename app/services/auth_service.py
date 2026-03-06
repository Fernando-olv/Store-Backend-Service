from fastapi import HTTPException
from passlib.context import CryptContext

from app.models.auth import LoginRequest, RegisterRequest, TokenResponse
from app.repositories.user_repository import UserRepository
from app.services.jwt_service import JWTService


class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(self, user_repository: UserRepository, jwt_service: JWTService) -> None:
        self._user_repository = user_repository
        self._jwt_service = jwt_service
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def register(self, payload: RegisterRequest) -> None:
        existing = self._user_repository.get_by_email(payload.email)
        if existing:
            raise UserAlreadyExistsError

        password_hash = self._pwd_context.hash(payload.password)
        self._user_repository.create_user(payload.email, password_hash)

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self._user_repository.get_by_email(payload.email)
        if not user:
            raise InvalidCredentialsError

        password_hash = user.get("password_hash")
        if not isinstance(password_hash, str) or not self._pwd_context.verify(payload.password, password_hash):
            raise InvalidCredentialsError

        token = self._jwt_service.create_access_token(subject=payload.email)
        return TokenResponse(access_token=token, expires_in=self._jwt_service.expiration_minutes * 60)


def invalid_credentials_http_exception() -> HTTPException:
    return HTTPException(status_code=401, detail="no valid credentials")
