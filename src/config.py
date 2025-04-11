from pydantic_settings import BaseSettings, SettingsConfigDict


class AppDomainSettings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    @property
    def APP_URL(self) -> str:
        return f"http://{self.APP_HOST}:{self.APP_PORT}"


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


AppDomainConfig = AppDomainSettings()
RedisConfig = RedisSettings()
