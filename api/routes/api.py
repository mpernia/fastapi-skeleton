from fastapi import APIRouter
from .user import router as user_router

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

router.include_router(user_router)
