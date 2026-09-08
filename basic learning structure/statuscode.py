from fastapi import FastAPI,status
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name: str
    category: str
    price: float
class ProductOut(BaseModel):
    name:str
    price: float

@app.post("/products",response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product:Product):
    return product

# status.HTTP_201_CREATED is just a readable constant equal to 201, instead of generic 200 now on success the response code will be 201 for this particular function/response.

@app.delete("/products/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id=int):
    # delete logic

    return # no body needed for 204