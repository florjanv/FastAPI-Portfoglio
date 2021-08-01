from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src import schemas, models, oauth2, crud
from fastapi.encoders import jsonable_encoder



router = APIRouter(
    prefix="/proj",
    tags=["Projects"]
)


@router.post("/post",  status_code=status.HTTP_201_CREATED)
def post_proj(response: Response, request: schemas.Projects,db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    new_proj = models.Projects(proj_name=request.proj_name,date_from=request.date_from,date_to=request.date_to, exp_id=request.exp_id)
    if not new_proj:
        response.staus_code = status.HTTP_501_NOT_IMPLEMENTED
    return crud.add_post(new_proj,db)



@router.get("/get", status_code=status.HTTP_202_ACCEPTED)
def get_proj(db:Session=Depends(crud.get_db)):
    return db.query(models.Projects).all()

@router.get("/get-{id}", status_code=status.HTTP_202_ACCEPTED)
def get_proj_by_id(id, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    proj_by_id = crud.queryDB_by_id(models.Projects,id,db).first()
    if not proj_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The project with id={id} do not exist.")
    return proj_by_id

@router.delete("/delete-{id}", status_code=status.HTTP_202_ACCEPTED)
def del_proj_by_id(id, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    proj = crud.queryDB_by_id(models.Projects,id,db).delete(synchronize_session=False)
    if not proj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The project with id={id} do not exist.")
    db.commit()
    return {"Details":f"project with ID={id} is deleted."}



@router.put("/update-{id}", status_code=status.HTTP_202_ACCEPTED)
def update_proj_by_id(id,request: schemas.Projects, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    proj = crud.queryDB_by_id(models.Projects,id,db).update(jsonable_encoder(request))
    if not proj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The project with id={id} do not exist.")
    db.commit()
    return {"Details":f"project with ID={id} is updated sucessfully."}