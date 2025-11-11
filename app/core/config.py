from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    OPENAI_API_KEY: str
    class Config:
        env_file = ".env"


settings = Settings()