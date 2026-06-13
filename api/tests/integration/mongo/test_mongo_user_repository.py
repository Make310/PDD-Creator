import asyncio

from expects import be_none, equal, expect, raise_error

from src.common.settings import settings
from src.domain.user import User, UserRole
from src.domain.user_repository import UserRepositoryException
from src.infrastructure.mongo.database import init_database
from src.infrastructure.mongo.mongo_user_repository import MongoUserRepository
from src.infrastructure.mongo.user_document import UserDocument

TEST_DATABASE = f"{settings.mongodb_database}_test"
USER = User(
    email="user@example.com",
    name="Jane Doe",
    role=UserRole.USER,
    is_active=True,
    password_hash="$2b$12$hashed-password",
)


class TestMongoUserRepository:
    async def _setup_clean_database(self) -> None:
        await init_database(
            mongodb_uri=settings.mongodb_uri,
            database_name=TEST_DATABASE,
            server_selection_timeout_ms=settings.mongodb_server_selection_timeout_ms,
        )
        await UserDocument.delete_all()

    def test_save_and_find_by_email_round_trips_the_user(self) -> None:
        async def scenario() -> User | None:
            await self._setup_clean_database()
            repository = MongoUserRepository()
            await repository.save(USER)
            return await repository.find_by_email(USER.email)

        found = asyncio.run(scenario())

        expect(found).to(equal(USER))

    def test_find_by_email_returns_none_for_unknown_email(self) -> None:
        async def scenario() -> User | None:
            await self._setup_clean_database()
            return await MongoUserRepository().find_by_email("nobody@example.com")

        found = asyncio.run(scenario())

        expect(found).to(be_none)

    def test_save_rejects_duplicated_email(self) -> None:
        async def scenario() -> None:
            await self._setup_clean_database()
            repository = MongoUserRepository()
            await repository.save(USER)
            await repository.save(USER)

        expect(lambda: asyncio.run(scenario())).to(raise_error(UserRepositoryException))
