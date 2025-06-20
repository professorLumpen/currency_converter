from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv())

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    CURRENCY_API_KEY: str
    CURRENCY_API_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def CURRENCY_API_LINK(self):
        return f"{self.CURRENCY_API_URL}live?access_key={self.CURRENCY_API_KEY}"

    @property
    def CURRENCY_API_LIST(self):
        return f"{self.CURRENCY_API_URL}list?access_key={self.CURRENCY_API_KEY}"


settings = Settings()
