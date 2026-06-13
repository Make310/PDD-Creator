from http.client import UNAUTHORIZED

from fastapi import APIRouter, Depends, HTTPException

from src.delivery.api.v1.auth.auth_dependencies import authenticated_user, login_command_handler
from src.delivery.api.v1.auth.auth_request import LoginRequest
from src.delivery.api.v1.auth.auth_response import LoginResponse, UserResponse
from src.domain.exceptions import InvalidCredentialsException
from src.domain.user import User
from src.use_cases.login_command import LoginCommand, LoginCommandHandler

LOGIN_FAILED_DETAIL = "Invalid credentials"

auth: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    handler: LoginCommandHandler = Depends(login_command_handler),
) -> LoginResponse:
    command = LoginCommand(email=request.email, password=request.password)
    try:
        response = await handler.execute(command)
    except InvalidCredentialsException as ex:
        raise HTTPException(status_code=UNAUTHORIZED, detail=LOGIN_FAILED_DETAIL) from ex

    auth_token = response.message()
    return LoginResponse(access_token=auth_token.access_token, expires_in=auth_token.expires_in_seconds)


@auth.get("/me", response_model=UserResponse)
async def me(user: User = Depends(authenticated_user)) -> UserResponse:
    return UserResponse(email=user.email, name=user.name, role=user.role)
