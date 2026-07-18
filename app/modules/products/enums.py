from enum import StrEnum


class ProductState(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    NO_STOCK = "NO_STOCK"
    DISCONTINUED = "DISCONTINUED"
