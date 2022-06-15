from fastapi import APIRouter
from .user import router as user_router
from api.config.resources import API_PREFIX

router = APIRouter(prefix=API_PREFIX)
router.include_router(user_router)

