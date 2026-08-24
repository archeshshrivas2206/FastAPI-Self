from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None=None # this is a way to declare an optional field {latest}
    desc: Optional[str]=None  # this is the older way of declaring an optional field
    in_stock: bool = True

from pydantic import Field
class Item2(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0) #gt means grater than 
    quantity: int = Field(ge=1, le=1000) # ge means greater than or equal to ; le = less than or equal to 

from pydantic import EmailStr , HttpUrl

class Users(BaseModel):
    name: str
    email: EmailStr # validates actual email format
    website: HttpUrl #validates it's a real url


# validating with regex/pattern

class Users2(BaseModel):
    username: str= Field(pattern=r"^[a-zA-Z0-9_]+$") # only letters, numbers, underscores are alloed , things enclosed in [] are the valid characters , + denote that there should be atleast one character from the [] , ^ and $ states the start and end of the string and r means raw string in python. 


# Nested Models 

class Address(BaseModel):
    city: str
    pincode: int

class User3(BaseModel):
    name: str
    email: EmailStr
    address: Address # nested model 



# List of models 
class Order(BaseModel):
    item_name: str
    quantity: int

class User4(BaseModel):
    name: str
    orders: list[Order]=[] # a list of Order objects, default to empty list.


# Custom Validators 

from pydantic import field_validator

class User5(BaseModel):
    name: str
    age: int

    @field_validator("age")
    @classmethod
    def check_age(cls,value):
        if value < 18:
            raise ValueError("You are underage! ")
        return value
    