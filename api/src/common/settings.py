from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"
    api_v1_prefix: str = "/api/v1"
    project_name: str = "PDD Creator API"
    description: str = "FastAPI BFF for PDD Creator — auth, job submission and PDD reads."
    logger_name: str = "api"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "pdd_creator"
    mongodb_server_selection_timeout_ms: int = 3000
    auth_secret_key: str = "dev-only-secret-change-me-in-production-0000"
    auth_token_ttl_minutes: int = 60


settings = Settings()
