from fastapi import APIRouter

from app.modules.events.router import router as events_router
from app.modules.products.router import router as products_router

router = APIRouter()
router.include_router(products_router)
router.include_router(events_router)
