from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    openrouter_api_key: str
    redis_host: str
    redis_port: int
    redis_db: int = 0
    redis_ttl_seconds: int = 86400

    class Config:
        env_file = ".env"


settings = Settings()
