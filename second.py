from pydantic import BaseModel
from fastapi import FastAPI

app=FastAPI()

class User(BaseModel):
    name:str
    email:str


@app.post("/users")
def create_user(user:User):
    return {"message": f"created a user with the name {user.name} and email {user.email}"}

#combining all this in one 

@app.post("/users/{user_id}/orders")
def update_orders(user_id: int , status: str, order:User):
    return{"user": user_id,"status":status,"order_name": order.name, "order_email": order.email}