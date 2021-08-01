from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src import schemas, models, hash_password, crud, oauth2
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

#create user related with database
@router.post("/post", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def post_users(response: Response, request: schemas.User,db:Session=Depends(crud.get_db)):
    new_user = models.User(nick_name=request.nick_name,email=request.email,hashed_password=hash_password.hash.bcrypt_hashing(request.hashed_password),is_active=request.is_active)
    if not new_user:
        response.staus_code = status.HTTP_501_NOT_IMPLEMENTED
    return crud.add_post(new_user,db)

#get all user information from database
@router.get("/get", status_code=status.HTTP_202_ACCEPTED, tags=["Users"])
def get_users(db:Session=Depends(crud.get_db)):
    return db.query(models.User).all()

#get user by ID
@router.get("/get-{id}", response_model=schemas.ShowUser, status_code=status.HTTP_202_ACCEPTED)
def get_users_by_id(id, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    user_by_id = crud.queryDB_by_id(models.User,id,db).first()
    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The User with id={id} do not exist.")
    return user_by_id

#delete user from database
@router.delete("/delete-{id}", status_code=status.HTTP_202_ACCEPTED)
def del_users_by_id(id,db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    user = crud.queryDB_by_id(models.User,id,db).delete(synchronize_session=False)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The user with id={id} do not exist.")
    db.commit()
    return {"Details":f"User with ID={id} is deleted."}


#Update user from database
@router.put("/update-{id}", status_code=status.HTTP_202_ACCEPTED)
def update_users_by_id(id,request: schemas.User, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    user = crud.queryDB_by_id(models.User,id,db).update(jsonable_encoder(request))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The user with id={id} do not exist.")
    db.commit()
    return {"Details":f"Skills with ID={id} is updated sucessfully."}
