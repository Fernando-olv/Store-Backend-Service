from app.services.jwt_service import JWTService, extract_subject


def test_jwt_create_and_extract_subject() -> None:
    service = JWTService(secret="test-secret", algorithm="HS256", expiration_minutes=60)
    token = service.create_access_token("buyer@example.com")

    subject = extract_subject(service, token)
    assert subject == "buyer@example.com"
