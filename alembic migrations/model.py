from sqlalchemy import Table, Column , Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
from database import Base


product_category=Table(
    "product_category",
    Base.metadata,
    Column("product_id",Integer,ForeignKey("product.id"),primary_key=True),
    Column("category_id",Integer,ForeignKey("category.id"),primary_key=True)
)


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
    stock_quantity=Column(Integer,default=0)

    manufacturer=relationship("Manufacturer",back_populates="products")
    categories=relationship("Category",secondary=product_category,back_populates="products")


class Category(Base):
    __tablename__="category"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False,unique=True)

    products=relationship("Product",secondary=product_category,back_populates="categories")

