from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "People Management API"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    RUN_SMOKE_TESTS: bool = True

    class Config:
        env_file = ".env"

settings = Settings()