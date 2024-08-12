from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql://user:password@host:port/database"
    )

    class Config:
        env_file = ".env"


settings = Settings()