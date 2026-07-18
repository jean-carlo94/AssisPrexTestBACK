from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.products.model import Product
from app.modules.products.schema import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Product]:
        return self.db.scalars(
            select(Product).offset(skip).limit(limit)
        ).all()

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def create(self, product_in: ProductCreate) -> Product:
        product = Product(**product_in.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, product_in: ProductUpdate) -> Product:
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()
