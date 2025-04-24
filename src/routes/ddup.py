from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.dependencies.redis import get_ddup_service
from src.schemas.event import EventSchema
from src.service.ddup import DeduplicationService

from src.worker.app import app

ddup_router = APIRouter()


@ddup_router.get("/test")
async def testing():
    return {"message": "successful"}


@ddup_router.post("/events")
async def process_event(
    event: EventSchema, service: DeduplicationService = Depends(get_ddup_service)
):
    if await service.is_duplicate(event):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate event detected",
        )

    app.send_task("process_event", args=[event.model_dump()])

    return JSONResponse(
        content={
            "status": "processed",
            "event": event.model_dump(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        status_code=status.HTTP_202_ACCEPTED
    )
