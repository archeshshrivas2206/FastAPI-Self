from database import Base, engine
import model
from fastapi import FastAPI

app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message":"value added to the db successfully "}