from sqlalchemy import Numeric, Column, Integer, String

from .database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10,2), nullable=False, index=True)