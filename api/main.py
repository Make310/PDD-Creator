from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.common.logger import logger
from src.common.settings import settings
from src.delivery.api.v1.health.health_router import health


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    logger.info("Starting FastAPI server...")

    yield

    logger.info("FastAPI server finished!")


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    lifespan=lifespan,
    openapi_url=settings.openapi_url,
)

app.include_router(prefix=settings.api_v1_prefix, router=health)
