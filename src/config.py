from pydantic_settings import BaseSettings, SettingsConfigDict


class AppDomainSettings(BaseSettings):
    APP_HOST: str
    APP_PORT: int

    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     extra="ignore",
    # )

    @property
    def APP_URL(self) -> str:
        return f"http://{self.APP_HOST}:{self.APP_PORT}"


class RedisSettings(BaseSettings):
    REDIS_DDUP_HOST: str
    REDIS_QUEUE_HOST: str
    REDIS_PORT: str
    EVENT_TTL: int

    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     extra="ignore",
    # )


class CelerySettings(BaseSettings):
    REDIS_DDUP_HOST: str
    REDIS_QUEUE_HOST: str
    REDIS_PORT: str

    # model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @property
    def CELERY_BROKER(self) -> str:
        return f"redis://{self.REDIS_QUEUE_HOST}:{self.REDIS_PORT}/0"
    
    @property
    def CELERY_BACKEND(self) -> str:
        return f"redis://{self.REDIS_QUEUE_HOST}:{self.REDIS_PORT}/1"
    
    @property
    def CELERY_DDUP_DB(self) -> str:
        return f"redis://{self.REDIS_DDUP_HOST}:{self.REDIS_PORT}/0"


AppDomainConfig = AppDomainSettings()
CeleryConfig = CelerySettings()
RedisConfig = RedisSettings()
