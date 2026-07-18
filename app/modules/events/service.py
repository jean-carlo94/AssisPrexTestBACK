from typing import Sequence

from app.modules.events.model import Event
from app.modules.events.repository import EventRepository


class EventService:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Event]:
        return self.event_repo.get_all(skip=skip, limit=limit)

    def get_by_id(self, event_id: int) -> Event | None:
        return self.event_repo.get_by_id(event_id)

    def get_by_product(
        self, product_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Event]:
        return self.event_repo.get_by_product(product_id, skip=skip, limit=limit)
