from fastapi import APIRouter

ddup_router = APIRouter()

@ddup_router.get("/test")
async def testing():
    return {"message": "successful"}