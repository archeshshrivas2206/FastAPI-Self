from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    price: float
    description: str | None=None # this is a way to declare an optional field {latest}
    # desc: Optional[str]=None  this is the older way of declaring an optional field
    in_stock= bool = True

from pydantic import Field
class Item2(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0) #gt means grater than 
    quantity: int = Field(ge=1, le=1000) # ge means greater than or equal to ; le = less than or equal to 

from pydantic import EmailStr , HttpUrl


