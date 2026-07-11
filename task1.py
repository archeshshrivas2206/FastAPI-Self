from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Items(BaseModel):
    name:str
    price:float


@app.get("/")
def get_homepage():
    return {"message": "Welcome to the home page"}

@app.get("/items")
def get_items(skip: int =0, limit:int=10):
    return{"skip": skip , "limit":limit}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return{"message": f"Found the item id {item_id}"}

@app.post("/items")
def create_item(items:Items):
    return {"message":f"the item with the name {items.name} and price {items.price} created/updated "}
