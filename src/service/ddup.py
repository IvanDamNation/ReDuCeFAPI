import hashlib
import json

from redis.asyncio import Redis

from src.schemas.event import EventSchema
from src.config import RedisConfig


class DeduplicationService:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.ttl = RedisConfig.EVENT_TTL

    async def _event_keygen(self, event: EventSchema) -> str:
        sorted_json = json.dumps(event.model_dump(), sort_keys=True)
        return hashlib.sha256(sorted_json.encode()).hexdigest()

    async def is_duplicate(self, event: EventSchema) -> bool:
        key = await self._event_keygen(event)
        return await self.redis.exists(key)

    async def register_event(self, event: EventSchema) -> None:
        key = await self._event_keygen(event)
        async with self.redis.pipeline() as pipe:
            exists, _ = await (
                pipe.exists(key).setex(name=key, time=self.ttl, value=1).execute()
            )
        return bool(exists)
