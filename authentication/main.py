import schemas
import model
import auth
from database import Base, engine , get_db
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session


app=FastAPI()


Base.metadata.create_all(bind=engine)

@app.get("/")
def homepage():
    return {"message":"welcome to homepage"}
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
