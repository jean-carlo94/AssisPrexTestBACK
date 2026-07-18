from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.events.deps import get_event_repository
from app.modules.events.repository import EventRepository
from app.modules.products.repository import ProductRepository
from app.modules.products.service import ProductService


def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository),
    event_repo: EventRepository = Depends(get_event_repository),
) -> ProductService:
    return ProductService(product_repo, event_repo)
