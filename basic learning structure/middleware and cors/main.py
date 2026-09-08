import schemas
import model
import auth

from database import Base, engine , get_db
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import time
from fastapi import Request

from fastapi.middleware.cors import CORSMiddleware




app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

@app.middleware("http")
async def log_requests(request:Request,call_next):
    start_time=time.time()
    response=await call_next(request)
    duration=time.time()-start_time
    print (f"{request.method}{request.url.path} completed in {duration:.4f}s")
    return response

@app.middleware("http")
async def add_process_time_header(request: Request,call_next):
    start_time=time.time()
    response=await call_next(request)
    process_time=time.time()- start_time
    response.headers["X-Process-Time"]=str(process_time)
    return response

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload=auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    username=payload.get("sub")
    user=db.query(model.User).filter(model.User.username==username).first()
    if user is None:
        raise HTTPException(status_code=401,detail="User not found")
    return user


@app.get("/")
def homepage():
    return {"message":"welcome to homepage"}


@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):

    user=db.query(model.User).filter(model.User.username==form_data.username).first()

    if not user or not auth.verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status=401,detail="Incorect username or password")
    
    access_token=auth.create_access_token(data={"sub":user.username})
    return {"access_token":access_token,"token_type":"bearer"}


@app.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(model.User).filter(model.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already taken")

    new_user = model.User(
        username=user.username,
        email=user.email,
        hashed_password=auth.hash_password(user.password)   # hash immediately, never store raw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/categories",response_model=schemas.CategoryOut,status_code=status.HTTP_201_CREATED)
def create_category(category:schemas.CategoryCreate,db:Session=Depends(get_db)):
    new_category=model.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.post("/products",response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product:schemas.ProductCreate,db:Session=Depends(get_db)):
    manufacturer=db.query(model.Manufacturer).filter(model.Manufacturer.id==product.manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="manufacturer not found")
    categories=db.query(model.Category).filter(model.Category.id.in_(product.category_ids)).all()
    
    new_product=model.Product(
        name=product.name,
        price=product.price,
        description=product.description,
        manufacturer_id=product.manufacturer_id,
        categories=categories

    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.post("/manufacturers",response_model=schemas.ManufacturerOut,status_code=status.HTTP_201_CREATED)
def create_manufacturer(manufacturer:schemas.ManufacturerCreate,db:Session=Depends(get_db)):
    new_manufacturer=model.Manufacturer(
        name=manufacturer.name,
        country=manufacturer.country
    )
    db.add(new_manufacturer)
    db.commit()
    db.refresh(new_manufacturer)
    return new_manufacturer



@app.get("/me",response_model=schemas.UserOut)
def read_current_user(current_user:model.User=Depends(get_current_user)):
    return current_user


@app.get("/products",response_model=list[schemas.ProductOut])
def get_products(db:Session=Depends(get_db)):
    return db.query(model.Product).all()


@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id:int,db:Session=Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/manufacturers/{manufacturer_id}/products", response_model=list[schemas.ProductOut])
def get_manufacturer_products(manufacturer_id:int,db:Session=Depends(get_db)):
    manufacturer=db.query(model.Manufacturer).filter(model.Manufacturer.id==manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="Manufacturer not found")
    return manufacturer.products


@app.get("/categories/{category_id}/products",response_model=list[schemas.ProductOut])
def get_category_products(category_id:int,db:Session=Depends(get_db)):
    category=db.query(model.Category).filter(model.Category.id==category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category.products


@app.put("/products/{product_id}",response_model=schemas.ProductOut)
def update_product(product_id:int ,updated:schemas.ProductCreate,db:Session=Depends(get_db)):
    product=db.query(model.Product).filter(model.Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="product not found")
    product.name=updated.name
    product.price=updated.price
    product.description=updated.description
    product.manufacturer_id=updated.manufacturer_id
    product.category_id=updated.category_id
    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id:int, db:Session=Depends(get_db)):
    product=db.query(model.Product).filter(model.Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    db.delete(product)
    db.commit()
    return

