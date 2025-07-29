from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.library_mgmt import api_user

router = APIRouter()

router.include_router(hello_world_router)
router.include_router(api_user.router)