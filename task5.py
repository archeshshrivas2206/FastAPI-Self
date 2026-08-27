from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

def get_pagination(skip:int=0,limit:int=10):
    return {"skip":skip,"limit":limit}

@app.get("/products")
def get_products(pagination:dict=Depends(get_pagination)):
    return pagination


def verify_admin(is_admin:bool=False):
    if is_admin is False:
        raise HTTPException(status_code=403,detail="You are not authorised admin")
    return is_admin

@app.delete("/products/{product_id}")
def delete_product(product_id:int,is_admin:bool=Depends(verify_admin)):
    
    #if is_admin is True: theres no need to do this as if the value is false the operation would stop at verify_admin function stage and hence it is the reason to use dependency so we dont have to check it again and again


        #delete logic
    
    return {"message":f"the product with id {product_id} is deleted"}
    