from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.events.deps import get_event_service
from app.modules.events.schema import EventResponse
from app.modules.events.service import EventService

router = APIRouter(tags=["events"])


@router.get("/events/", response_model=list[EventResponse])
def list_events(
    skip: int = 0,
    limit: int = 100,
    service: EventService = Depends(get_event_service),
) -> Sequence[EventResponse]:
    return service.get_all(skip=skip, limit=limit)


@router.get("/events/{event_id}", response_model=EventResponse)
def retrieve_event(
    event_id: int,
    service: EventService = Depends(get_event_service),
) -> EventResponse:
    event = service.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    return event


@router.get("/products/{product_id}/events/", response_model=list[EventResponse])
def list_product_events(
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    service: EventService = Depends(get_event_service),
) -> Sequence[EventResponse]:
    return service.get_by_product(product_id, skip=skip, limit=limit)
