"""Create the first admin user directly against MongoDB, without using the API.

Usage (from api/):
    uv run python -m src.delivery.cli.create_admin --email admin@example.com --name "Admin"

The password is read from the ADMIN_PASSWORD environment variable or prompted
interactively — it is never accepted as a command-line argument so it does not
leak into the shell history or process list.
"""

import argparse
import asyncio
import os
import sys
from getpass import getpass

from src.common.logger import logger
from src.common.settings import settings
from src.domain.exceptions import UserAlreadyExistsException
from src.infrastructure.mongo.database import DatabaseInitializationException, init_database
from src.infrastructure.mongo.mongo_user_repository import MongoUserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.use_cases.create_admin_user_command import CreateAdminUserCommand, CreateAdminUserCommandHandler

PASSWORD_ENV_VAR = "ADMIN_PASSWORD"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create the first admin user without using the API")
    parser.add_argument("--email", required=True, help="Admin email (unique)")
    parser.add_argument("--name", required=True, help="Admin display name")
    return parser.parse_args()


def _read_password() -> str:
    password = os.environ.get(PASSWORD_ENV_VAR) or getpass("Admin password: ")
    if not password:
        logger.error("Password cannot be empty")
        sys.exit(1)
    return password


async def _create_admin(email: str, name: str, password: str) -> None:
    await init_database(
        mongodb_uri=settings.mongodb_uri,
        database_name=settings.mongodb_database,
        server_selection_timeout_ms=settings.mongodb_server_selection_timeout_ms,
    )
    handler = CreateAdminUserCommandHandler(
        user_repository=MongoUserRepository(), password_hasher=BcryptPasswordHasher()
    )
    command = CreateAdminUserCommand(email=email, name=name, password=password)
    response = await handler.execute(command)
    logger.info(f"Admin user created: {response.message()}")


def main() -> None:
    args = _parse_args()
    password = _read_password()
    try:
        asyncio.run(_create_admin(email=args.email, name=args.name, password=password))
    except DatabaseInitializationException as ex:
        logger.error(f"Could not connect to MongoDB: {ex}")
        sys.exit(1)
    except UserAlreadyExistsException as ex:
        logger.error(str(ex))
        sys.exit(1)


if __name__ == "__main__":
    main()
