from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.common.logger import logger
from src.common.settings import settings
from src.delivery.api.v1.auth.auth_router import auth
from src.delivery.api.v1.health.health_router import health
from src.infrastructure.mongo.database import DatabaseInitializationException, init_database


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    logger.info("Starting FastAPI server...")

    try:
        await init_database(
            mongodb_uri=settings.mongodb_uri,
            database_name=settings.mongodb_database,
            server_selection_timeout_ms=settings.mongodb_server_selection_timeout_ms,
        )
        logger.info("MongoDB initialized")
    except DatabaseInitializationException as ex:
        logger.warning(f"MongoDB unavailable, database-backed endpoints will fail: {ex}")

    yield

    logger.info("FastAPI server finished!")


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    lifespan=lifespan,
    openapi_url=settings.openapi_url,
)

app.include_router(prefix=settings.api_v1_prefix, router=health)
app.include_router(prefix=settings.api_v1_prefix, router=auth)
