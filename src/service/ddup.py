import hashlib
import json

from redis.asyncio import Redis

from schemas.event import EventSchema

class DeduplicationService:
    def __init__(self, redis: Redis):
        self.redis = redis
        
    async def _event_keygen(self, event: EventSchema) -> str:
        sorted_json = json.dumps(event.model_dump(), sort_keys=True)
        return hashlib.sha256(sorted_json.encode()).hexdigest()
    
    async def is_duplicate(self, event: EventSchema) -> bool:
        pass
    
    async def register_event(self, event: EventSchema) -> None:
        pass