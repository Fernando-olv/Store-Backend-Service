import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    firestore_project_id: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_expiration_minutes: int


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    firestore_project_id = os.getenv("FIRESTORE_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not firestore_project_id:
        raise RuntimeError("FIRESTORE_PROJECT_ID or GOOGLE_CLOUD_PROJECT must be set")

    jwt_secret = os.getenv("JWT_SECRET")
    if not jwt_secret:
        raise RuntimeError("JWT_SECRET must be set")

    return Settings(
        firestore_project_id=firestore_project_id,
        jwt_secret=jwt_secret,
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        jwt_expiration_minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", "60")),
    )
