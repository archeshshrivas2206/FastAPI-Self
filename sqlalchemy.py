from sqlalchemy import Column, Integer, String, Float
from databasetutorial import Base

class Product(Base):
    __tablename__="products"

    id=Column(Integer,primary_key=True,index=True)
    name= Column(String(100), nullable=False) 
    price= Column(Float,nullable=False)
    description=Column(String(250),nullable=True)

