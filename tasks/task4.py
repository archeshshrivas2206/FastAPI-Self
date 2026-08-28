from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name:str
    category:str
    price:float
    manufacturer:str

class ProductOut(BaseModel):
    name: str
    price: float

temp_db = {}
next_id = 1

@app.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    global next_id
    new_product = {"id": next_id, "name": product.name, "price": product.price}
    temp_db[next_id] = new_product
    next_id += 1
    return new_product

@app.get("/products/{product_id}", response_model=ProductOut)
def check_product(product_id:int):
    if product_id not in temp_db:
        raise HTTPException(status_code=404,detail="Product not found")
    return temp_db[product_id]