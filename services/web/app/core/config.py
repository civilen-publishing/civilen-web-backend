from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: Optional[str] = ""
    PROJECT_VERSION: Optional[str] = "1.0.0"
    PROJECT_ENVIRONMENT: str

    BACKEND_CORS_ORIGINS: List[str] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, value: Optional[PostgresDsn], values: Dict[str, Any]) -> Any:
        if isinstance(value, PostgresDsn):
            return value

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=f"/{values.get('DB_DATABASE') or ''}",
        )

    SP_API_REFRESH_TOKEN: str
    SP_API_LWA_APP_ID: str
    SP_API_LWA_CLIENT_SECRET: str
    SP_API_AWS_SECRET_KEY: str
    SP_API_AWS_ACCESS_KEY: str
    SP_API_ROLE_ARN: str
    SP_API_SELLER_ID: str

    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str

    DOMAIN_NAME: Optional[str] = "http://127.0.0.1:8000"

    AUTH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    EMAIL_SERVICE_URL: str
    EMAIL_SERVICE_ID: str
    EMAIL_SERVICE_TEMPLATE_ID: str
    EMAIL_SERVICE_USER_ID: str

    SHIPBOB_API_EMAIL: str
    SHIPBOB_API_TOKEN_ID: str
    SHIPBOB_API_TOKEN: str

    class Config:
        case_sensitive = True
        env_file = "../env"


# This is a decorator that caches the result of the function
# so that it doesn't have to be called again
@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
