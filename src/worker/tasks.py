import asyncio
import logging
from pydantic import ValidationError
from redis.asyncio import Redis

from src.config import CeleryConfig
from src.schemas.event import EventSchema
from src.service.ddup import DeduplicationService
from src.worker.app import app


logger = logging.getLogger(__name__)


async def get_service():
    ddup_redis = Redis.from_url(CeleryConfig.CELERY_DDUP_DB)
    return DeduplicationService(ddup_redis)


@app.task(bind=True, max_retries=3, name="process_event", pydantic=True)
def process_event(self, event_data: dict):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logger.info(f"Received task: {self.request.id}, Event: {event_data}")

    try:
        service = loop.run_until_complete(get_service())
        event = EventSchema(**event_data)
        logger.debug(f"Processing event: {event}")

        is_duplicate = loop.run_until_complete(service.is_duplicate(event))
        if is_duplicate:
            logger.warning(f"Duplicate detected: {event}")
            return {"status": "duplicate"}

        loop.run_until_complete(service.register_event(event))
        logger.info(f"Event processed: {event}")
        return {"status": "processed"}

    except ValidationError as e:
        self.retry(exc=e, countdown=2**self.request.retries)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        self.retry(exc=e, countdown=2**self.request.retries)
    finally:
        loop.close()
        asyncio.set_event_loop(None)
