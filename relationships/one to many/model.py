from sqlalchemy import Integer,Float,String,Column,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Manufacturer(Base):
    __tablename__="manufacturer"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    country=Column(String(50),nullable=False)
    products=relationship("Product",back_populates="manufacturer")

class Product(Base):
    __tablename__="product"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    price=Column(Float,nullable=False)
    description=Column(String(250),nullable=True)
    manufacturer_id=Column(Integer,ForeignKey("manufacturer.id"))
    manufacturer=relationship("Manufacturer",back_populates="products")
