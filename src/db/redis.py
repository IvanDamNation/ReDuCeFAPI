from redis import asyncio as aioredis

from src.config import RedisConfig

hash_blocklist = aioredis.StrictRedis(
    host=RedisConfig.REDIS_HOST, port=RedisConfig.REDIS_PORT, db=0
)


async def add_hash():
    pass


async def is_blocked():
    pass
