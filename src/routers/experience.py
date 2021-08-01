from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src import schemas, models, oauth2, crud
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/exp",
    tags=["Experience"]
)


@router.post("/post",  status_code=status.HTTP_201_CREATED)
def post_exp(response: Response, request: schemas.Experience,db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    new_exp = models.Experience(date_from=request.date_from,date_to=request.date_to,employer=request.employer,website=request.website,job_description=request.job_description,job_position=request.job_position)
    if not new_exp:
        response.staus_code = status.HTTP_501_NOT_IMPLEMENTED
    return crud.add_post(new_exp,db)


@router.get("/get", status_code=status.HTTP_202_ACCEPTED)
def get_exp(db:Session=Depends(crud.get_db)):
    return db.query(models.Experience).all()

@router.get("/get-{id}", status_code=status.HTTP_202_ACCEPTED)
def get_exp_by_id(id, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    exp_by_id = crud.queryDB_by_id(models.Experience,id,db).first()
    if not exp_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Experience with id={id} do not exist.")
    return exp_by_id

@router.delete("/delete-{id}", status_code=status.HTTP_202_ACCEPTED)
def del_exp_by_id(id,db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    exp = crud.queryDB_by_id(models.Experience,id,db).delete(synchronize_session=False)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The experience with id={id} do not exist.")
    db.commit()
    return {"Details":f"Experience with ID={id} is deleted."}

@router.put("/update-{id}", status_code=status.HTTP_202_ACCEPTED)
def update_exp_by_id(id,request: schemas.Experience, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    exp = crud.queryDB_by_id(models.Experience,id,db).update(jsonable_encoder(request))
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The experience with id={id} do not exist.")
    db.commit()
    return {"Details":f"Experience with ID={id} is updated sucessfully."}