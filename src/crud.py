from src import models
from src.database import engine,SessionLocal

#create the database connection
models.Base.metadata.create_all(engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#add post into database
def add_post(new_post,db):
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def queryDB_by_id(model_db,id,db):
    return db.query(model_db).filter(model_db.id == id)