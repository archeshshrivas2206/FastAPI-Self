from pydantic import BaseModel

class ProductCreate(BaseModel):
    name:str
    price:float
    description:str|None=None

class ProductOut(BaseModel):
    id:int
    name:str
    price:float
    description:str|None=None

    class Config:
        from_attributes=True


