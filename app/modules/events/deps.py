from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.events.repository import EventRepository
from app.modules.events.service import EventService


def get_event_repository(db: Session = Depends(get_db)) -> EventRepository:
    return EventRepository(db)


def get_event_service(
    event_repo: EventRepository = Depends(get_event_repository),
) -> EventService:
    return EventService(event_repo)
