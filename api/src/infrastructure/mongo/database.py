from beanie import init_beanie
from pymongo import AsyncMongoClient
from pymongo.errors import PyMongoError

from src.infrastructure.mongo.user_document import UserDocument

DOCUMENT_MODELS = [UserDocument]


class DatabaseInitializationException(Exception):
    pass


async def init_database(mongodb_uri: str, database_name: str, server_selection_timeout_ms: int) -> None:
    client: AsyncMongoClient = AsyncMongoClient(mongodb_uri, serverSelectionTimeoutMS=server_selection_timeout_ms)
    try:
        await init_beanie(database=client[database_name], document_models=DOCUMENT_MODELS)
    except PyMongoError as ex:
        raise DatabaseInitializationException(str(ex)) from ex
