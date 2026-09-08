from fastapi import FastAPI , Depends

app = FastAPI()

def get_query_params(skip: int = 0, limit: int=10):
    return {"skip": skip, "limit": limit}

@app.get("/products")
def get_products(params:dict=Depends(get_query_params)): # the return value of the function get_query_params is used here as a parameter

    return params


# real world example 

from fastapi import HTTPException


fake_db={"validuser1":{"id": 1,"name":"archesh"}}

def get_current_user(token:str):
    if token not in fake_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    return fake_db[token]

@app.get("/profile")
def read_profile(current_user: dict=Depends(get_current_user)):
    return {"message":f"Welcome! {current_user['name']}"}

@app.get("/orders")
def read_orders(current_user: dict=Depends(get_current_user)):
    return {"message": f"order for {current_user['name']}"}


# dependency depending on other dependencies


def get_token(authorization: str=""):
    return authorization.replace("Bearer","")

def get_current_user2(token:str=Depends(get_token)):
    if token not in fake_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    return fake_db[token]

@app.get("/profile")
def get_profile(current_user:dict=Depends(get_current_user2)):
    return current_user

# here the get_profile is injecting dependency from get_current_users2 which itself is injecting dependency from get_token

# class based dependency 

class Paginator:
    def __init__(self, skip: int = 0, limit:int=10):
    
        self.skip=skip
        self.limit=limit

@app.get("/products")
def get_products(pagination: Paginator=Depends(Paginator)):
    return{"skip": pagination.skip, "limit": pagination.limit}
