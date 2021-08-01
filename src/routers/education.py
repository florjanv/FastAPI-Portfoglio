from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src import schemas, models, oauth2, crud
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/edu",
    tags=["Education"]
)

@router.post("/post",  status_code=status.HTTP_201_CREATED)
def post_edu(response: Response, request: schemas.Education,db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    new_edu = models.Education(ed_type=request.ed_type,ed_title=request.ed_title,ed_place=request.ed_place,website=request.website,date_from=request.date_from,date_to=request.date_to,active=request.active)
    if not new_edu:
        response.staus_code = status.HTTP_501_NOT_IMPLEMENTED
    return crud.add_post(new_edu,db)


@router.get("/get", status_code=status.HTTP_202_ACCEPTED)
def get_edu(db:Session=Depends(crud.get_db)):
    return db.query(models.Education).all()

@router.get("/get-{id}", status_code=status.HTTP_202_ACCEPTED)
def get_edu_by_id(id, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    edu_by_id = crud.queryDB_by_id(models.Education,id,db).first()
    if not edu_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Education with id={id} do not exist.")
    return edu_by_id

@router.delete("/delete-{id}", status_code=status.HTTP_202_ACCEPTED)
def del_edu_by_id(id,db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    edu = crud.queryDB_by_id(models.Education,id,db).delete(synchronize_session=False)
    if not edu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The education with id={id} do not exist.")
    db.commit()
    return {"Details":f"Education with ID={id} is deleted."}


@router.put("/update-{id}", status_code=status.HTTP_202_ACCEPTED)
def update_edu_by_id(id,request: schemas.Education, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    edu = crud.queryDB_by_id(models.Education,id,db).update(jsonable_encoder(request))
    if not edu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The education with id={id} do not exist.")
    db.commit()
    return {"Details":f"Education with ID={id} is updated sucessfully."}