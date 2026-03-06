from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.auth_service import invalid_credentials_http_exception
from app.services.container import get_jwt_service
from app.services.jwt_service import InvalidTokenError, extract_subject

_bearer = HTTPBearer(auto_error=False)


def get_current_user_email(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise invalid_credentials_http_exception()

    try:
        return extract_subject(get_jwt_service(), credentials.credentials)
    except InvalidTokenError as exc:
        raise invalid_credentials_http_exception() from exc
