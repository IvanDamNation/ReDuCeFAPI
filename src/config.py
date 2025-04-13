from pydantic_settings import BaseSettings, SettingsConfigDict


class AppDomainSettings(BaseSettings):
    APP_HOST: str
    APP_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def APP_URL(self) -> str:
        return f"http://{self.APP_HOST}:{self.APP_PORT}"


class RedisSettings(BaseSettings):
    REDIS_DDUP_HOST: str
    REDIS_DDUP_PORT: str
    REDIS_QUEUE_HOST: str
    REDIS_QUEUE_PORT: str
    EVENT_TTL: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


class CelerySettings(BaseSettings):
    CELERY_BROKER: str
    CELERY_BACKEND: str
    CELERY_DDUP_DB: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


AppDomainConfig = AppDomainSettings()
CeleryConfig = CelerySettings()
RedisConfig = RedisSettings()
