from redis import Redis, asyncio as aioredis

from src.config import RedisConfig


class RedisManager:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        self.pool = aioredis.StrictRedis(
            host=RedisConfig.REDIS_DDUP_HOST,
            port=RedisConfig.REDIS_PORT,
            db=0,
            decode_responses=True,
        )

    async def get_connection(self) -> Redis:
        if not self.pool:
            await self.init_pool()
        return self.pool


redis_manager = RedisManager()
