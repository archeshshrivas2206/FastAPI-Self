from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    price: float
    description: str | None=None # this is a way to declare an optional field {latest}
    desc: Optional[str]=None # this is the older way of declaring an optional field
    in_stock= bool = True

