import schemas
import model
from database import Base, engine , get_db
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session


app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/products",response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product:schemas.ProductCreate,db:Session=Depends(get_db)):
    new_product=model.Product(
        name=product.name,
        price=product.price,
        description=product.description
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products",response_model=list[schemas.ProductOut])
def get_products(db:Session=Depends(get_db)):
    return db.query(model.Product).all()

@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id:int,db:Session=Depends(get_db)):
    return db.query(model.Product).filter(model.Product.id==product_id).first()

@app.put("/products/{product_id}",response_model=schemas.ProductOut)
def update_product(product_id:int ,updated:schemas.ProductCreate,db:Session=Depends(get_db)):
    product=db.query(model.Product).filter(model.Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="product not found")
    product.name=updated.name
    product.price=updated.price
    product.description=updated.description
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