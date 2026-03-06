from fastapi import APIRouter, Depends, HTTPException, status

from app.models.auth import AuthMessageResponse, LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import AuthService, InvalidCredentialsError, UserAlreadyExistsError
from app.services.container import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthMessageResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)) -> AuthMessageResponse:
    try:
        auth_service.register(payload)
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail="user already exists") from exc
    return AuthMessageResponse(message="user created")


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, auth_service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    try:
        return auth_service.login(payload)
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=401, detail="no valid credentials") from exc
