from sqlalchemy.orm import Session

from . import models, schemas


def get_products(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
  new_product = models.Product(
    name=product.name, 
    price=product.price
  )
  db.add(new_product)
  db.commit()
  db.refresh(new_product)
  return new_product
