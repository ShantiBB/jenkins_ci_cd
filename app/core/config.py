from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    user: str
    password: str
    host: str
    port: str
    db_name: str

    @property
    def url(self):
        """Формирует путь для настройки БД"""
        return (
            f'postgresql+asyncpg://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.db_name}'
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter = '__',
    )

    postgres: PostgresSettings


settings = Settings()
