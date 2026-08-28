from database import Base
from sqlalchemy import Column, Integer, Float, String



class Product(Base):
    __tablename__="product"
    id= Column(Integer,primary_key=True,index=True)
    name= Column(String(100),nullable=False)
    price=Column(Float,nullable=False)
    description=Column(String(250),nullable=True)
