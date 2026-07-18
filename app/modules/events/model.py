from datetime import datetime

from sqlalchemy import Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.modules.events.enums import ActionType


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    action: Mapped[ActionType] = mapped_column(
        Enum(ActionType, name="action_type"), nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, default=None)
    create_at: Mapped[datetime] = mapped_column(
        "createAt", server_default=func.now(), nullable=False
    )
