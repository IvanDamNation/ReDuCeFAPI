from fastapi import Depends
from redis.asyncio import Redis

from src.db.redis import redis_manager
from src.service.ddup import DeduplicationService


async def get_redis() -> Redis:
    if not redis_manager.pool:
        await redis_manager.init_pool()
    return await redis_manager.get_connection()


async def get_ddup_service(redis: Redis = Depends(get_redis)) -> DeduplicationService:
    return DeduplicationService(redis)
