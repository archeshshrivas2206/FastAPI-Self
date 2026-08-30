import schemas
import model
from database import Base, engine , get_db
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session


app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/products",response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product:schemas.ProductCreate,db:Session=Depends(get_db)):
    manufacturer=db.query(model.Manufacturer).filter(model.Manufacturer.id==product.manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="manufacturer not found")
    
    new_product=model.Product(
        name=product.name,
        price=product.price,
        description=product.description,
        manufacturer_id=product.manufacturer_id
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
    return db.query(model.Product).filter(model.Product.id==product_id).first()

@app.get("/manufacturers/{manufacturer_id}/products", response_model=list[schemas.ProductOut])
def get_manufacturer_products(manufacturer_id:int,db:Session=Depends(get_db)):
    manufacturer=db.query(model.Manufacturer).filter(model.Manufacturer.id==manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="Manufacturer not found")
    return manufacturer.products

@app.put("/products/{product_id}",response_model=schemas.ProductOut)
def update_product(product_id:int ,updated:schemas.ProductCreate,db:Session=Depends(get_db)):
    product=db.query(model.Product).filter(model.Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="product not found")
    product.name=updated.name
    product.price=updated.price
    product.description=updated.description
    product.manufacturer_id=updated.manufacturer_id
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