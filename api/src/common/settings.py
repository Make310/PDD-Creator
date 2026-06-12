from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"
    api_v1_prefix: str = "/api/v1"
    project_name: str = "PDD Creator API"
    description: str = "FastAPI BFF for PDD Creator — auth, job submission and PDD reads."
    logger_name: str = "api"


settings = Settings()
