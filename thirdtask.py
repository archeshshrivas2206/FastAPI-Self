from pydantic import BaseModel, Field
from typing import Optional
from fastapi import FastAPI

app=FastAPI()


class Manufacturer(BaseModel):
    name : str
    country: str

class Product(BaseModel):
    name : str = Field(min_length=3 , max_length=100)
    price: float = Field(gt=0)
    description: Optional[str]=None
    tags: list[str]=[]
    manufacturer: Manufacturer 


@app.post("/products")
def posting_product(product:Product):
    return{"message": "Product added successfully", "product" : product}
