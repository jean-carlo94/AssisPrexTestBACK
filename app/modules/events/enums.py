from enum import StrEnum


class ActionType(StrEnum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    STATUS_CHANGED = "STATUS_CHANGED"
