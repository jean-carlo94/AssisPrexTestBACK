from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.events.enums import ActionType
from app.modules.events.model import Event


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        product_id: int,
        action: ActionType,
        description: str | None = None,
    ) -> Event:
        event = Event(product_id=product_id, action=action, description=description)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_all(self, skip: int = 0, limit: int = 100) -> tuple[Sequence[Event], int]:
        total = self.db.scalar(select(func.count()).select_from(Event))
        items = self.db.scalars(
            select(Event).order_by(Event.create_at.desc()).offset(skip).limit(limit)
        ).all()
        return items, total

    def get_by_id(self, event_id: int) -> Event | None:
        return self.db.get(Event, event_id)

    def get_by_product(
        self, product_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[Sequence[Event], int]:
        base = select(Event).where(Event.product_id == product_id)
        total = self.db.scalar(
            select(func.count()).select_from(base.subquery())
        )
        items = self.db.scalars(
            base.order_by(Event.create_at.desc()).offset(skip).limit(limit)
        ).all()
        return items, total
