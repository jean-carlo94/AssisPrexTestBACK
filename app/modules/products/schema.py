from datetime import datetime

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, examples=["Laptop"])
    description: str | None = Field(
        default=None, examples=["Laptop de alto rendimiento"]
    )
    price: float = Field(..., gt=0, examples=[999.99])
    stock: int = Field(default=0, ge=0, examples=[10])
    state: str = Field(default="active", examples=["active"])


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    state: str | None = None


class ProductResponse(ProductBase):
    id: int
    create_at: datetime

    model_config = {"from_attributes": True}
