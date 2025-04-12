from asgiref.sync import async_to_sync
from pydantic import ValidationError
from redis.asyncio import Redis

from src.config import CeleryConfig
from src.schemas.event import EventSchema
from src.service.ddup import DeduplicationService
from src.worker.app import app

@app.task(bind=True, max_retries=3)
def process_event(self, event_data: dict):
    try:
        try:
            event = EventSchema(**event_data)
        except ValidationError as e:
            self.retry(exc=e, countdown=2**self.request.retries)
        
        ddup_redis = Redis.from_url(CeleryConfig.CELERY_DDUP_DB)
        service = DeduplicationService(ddup_redis)
        
        if async_to_sync(service.is_duplicate)(event_data):
            return {"status": "duplicate"}
        
        async_to_sync(service.register_event)(event_data)
        return {"status": "processed"}
    
    except Exception as e:
        self.retry(exc=e, countdown=2**self.request.retries)
