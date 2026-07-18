from datetime import datetime

from pydantic import BaseModel

from app.modules.events.enums import ActionType


class EventResponse(BaseModel):
    id: int
    product_id: int
    action: ActionType
    description: str | None = None
    create_at: datetime

    model_config = {"from_attributes": True}
