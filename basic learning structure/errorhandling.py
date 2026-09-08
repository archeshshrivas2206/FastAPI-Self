from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app=FastAPI()

class Product(BaseModel):
    name:str
    category: str
    price:float

fake_db={1:{"name":"Keyboard","price":1500}}

@app.get("/products/{product_id}")
def get_product(product_id:int):
    if product_id not in fake_db:
        raise HTTPException(status_code=404,detail="Product not found")
    return fake_db[product_id]


