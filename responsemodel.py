from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Product(BaseModel):
    name:str
    category:str
    price:float

class ProductOut(BaseModel):
    name: str
    price: float

@app.post("/products",response_model=ProductOut) # response_model=ProductOut tells fastapi that the return value should be filtered valideted and serialized to exactly the shape of ProductOut . 
def create_product(product:Product):
    return product

# another real life use case 

class User(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    username: str 
    email: str

@app.post("/Users", response_model=UserOut)
def create_user(user:User):
    # any logic you want to perform
    return user
# even though 'user' has password field , its automatically excluded!
