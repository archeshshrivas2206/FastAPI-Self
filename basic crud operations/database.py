from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DARABASE_URL="mysql+pymsql://root:Archesh%400110@localhost:3306/app_db"

engine=create_engine(DARABASE_URL)
SessionLocal=sessionmaker(autocommit=False , autoflush=False,bind=engine)
Base=declarative_base()

def get_db():
    db=SessionLocal
    try:
        yield db
    finally:
        db.close()
