from http.client import UNAUTHORIZED

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.common.settings import settings
from src.domain.exceptions import InvalidTokenException
from src.domain.password_hasher import PasswordHasher
from src.domain.token_service import TokenService
from src.domain.user import User
from src.domain.user_repository import UserRepository
from src.infrastructure.mongo.mongo_user_repository import MongoUserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_token_service import JwtTokenService
from src.use_cases.authenticate_user_command import AuthenticateUserCommand, AuthenticateUserCommandHandler
from src.use_cases.login_command import LoginCommandHandler

UNAUTHORIZED_DETAIL = "Invalid or expired token"
UNAUTHENTICATED_HEADERS = {"WWW-Authenticate": "Bearer"}

bearer_scheme = HTTPBearer(auto_error=False)


async def user_repository() -> UserRepository:
    return MongoUserRepository()


async def password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


async def token_service() -> TokenService:
    return JwtTokenService(secret_key=settings.auth_secret_key, ttl_minutes=settings.auth_token_ttl_minutes)


async def login_command_handler(
    repository: UserRepository = Depends(user_repository),
    hasher: PasswordHasher = Depends(password_hasher),
    tokens: TokenService = Depends(token_service),
) -> LoginCommandHandler:
    return LoginCommandHandler(user_repository=repository, password_hasher=hasher, token_service=tokens)


async def authenticate_user_command_handler(
    repository: UserRepository = Depends(user_repository),
    tokens: TokenService = Depends(token_service),
) -> AuthenticateUserCommandHandler:
    return AuthenticateUserCommandHandler(user_repository=repository, token_service=tokens)


async def authenticated_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    handler: AuthenticateUserCommandHandler = Depends(authenticate_user_command_handler),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=UNAUTHORIZED, detail=UNAUTHORIZED_DETAIL, headers=UNAUTHENTICATED_HEADERS)

    command = AuthenticateUserCommand(token=credentials.credentials)
    try:
        response = await handler.execute(command)
    except InvalidTokenException as ex:
        raise HTTPException(
            status_code=UNAUTHORIZED, detail=UNAUTHORIZED_DETAIL, headers=UNAUTHENTICATED_HEADERS
        ) from ex
    return response.message()
