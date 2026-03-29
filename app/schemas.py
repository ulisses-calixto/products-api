from decimal import Decimal
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

