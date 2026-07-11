from fastapi import FastAPI

app= FastAPI()

@app.get("/")
def read_root():
    return {"message": "hello"}
# these are path params:

# this is more specific route function so it is placed above the dynamic one otherwise the dynamic function would have engulfed the 'me' and the sactual designated function for this url wouldnt have functioned. 

@app.get("/users/me") 
def get_me():
    return {"message": "this is a message for me "}

# this is a dynamic route function it is placed below static route functions so that it does not engulf the url it is not supposed to.  
@app.get("/users/{user_id}")
def get_usesrs(user_id: int):
    return {"usesrs_id" : user_id, "message": f"fetched {user_id}"}

# these are query params

#  this is a function with default values , this way the url without a ? will also run without any 422 error response ,

@app.get('/products')
def get_product(category: str= None, limit : int =10):
    return {"category": category , "limit": limit}

# this is a function which does not have any by default values so a url without '?' will give 422 error 
@app.get('/search')
def get_something(q:str):
    return {"query": q}