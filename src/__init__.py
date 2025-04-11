from fastapi import FastAPI

from src.routes.ddup import ddup_router

version = "v1"

app = FastAPI(
    title="Deduplicator",
    description="Deduplication service for product events",
    version=version,
)

app.include_router(
    ddup_router, prefix=f"/api/{version}/ddup_service", tags=["ddup_service"]
)
