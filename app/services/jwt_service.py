from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt


class JWTService:
    def __init__(self, secret: str, algorithm: str, expiration_minutes: int) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expiration_minutes = expiration_minutes

    @property
    def expiration_minutes(self) -> int:
        return self._expiration_minutes

    def create_access_token(self, subject: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._expiration_minutes)).timestamp()),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(token, self._secret, algorithms=[self._algorithm])


class InvalidTokenError(Exception):
    pass


def extract_subject(jwt_service: JWTService, token: str) -> str:
    try:
        payload = jwt_service.decode_access_token(token)
    except JWTError as exc:
        raise InvalidTokenError from exc

    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise InvalidTokenError
    return subject
