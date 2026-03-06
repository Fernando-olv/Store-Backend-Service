from functools import lru_cache

from google.cloud import firestore

from app.services.settings import get_settings


@lru_cache(maxsize=1)
def get_firestore_client() -> firestore.Client:
    settings = get_settings()
    return firestore.Client(project=settings.firestore_project_id)
