from pydantic import BaseModel

class ManufacturerCreate(BaseModel):
    name:str
    country:str

class ManufacturerOut(BaseModel):
    id:int
    name:str
    country:str

    class Config:
        from_attributes=True


class CategoryCreate(BaseModel):
    name:str

class CategoryOut(BaseModel):
    id:int
    name:str

    class Config:
        from_attributes=True


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str | None = None
    manufacturer_id:int
    category_ids:list[int]

class ProductOut(BaseModel):
    id:int
    name:str
    price:float
    description:str | None=None
    manufacturer:ManufacturerOut
    categories:list[CategoryOut]=[]
    

    class Config:
        from_attributes=True




