from pymongo.errors import PyMongoError

from src.domain.user import User
from src.domain.user_repository import UserRepository, UserRepositoryException
from src.infrastructure.mongo.user_document import UserDocument


class MongoUserRepository(UserRepository):
    async def find_by_email(self, email: str) -> User | None:
        try:
            document = await UserDocument.find_one(UserDocument.email == email)
        except PyMongoError as ex:
            raise UserRepositoryException(str(ex)) from ex
        return document.to_domain() if document is not None else None

    async def save(self, user: User) -> None:
        try:
            await UserDocument.from_domain(user).insert()
        except PyMongoError as ex:
            raise UserRepositoryException(str(ex)) from ex
