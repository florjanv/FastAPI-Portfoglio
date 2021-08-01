from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src import schemas, models, oauth2, crud
from fastapi.encoders import jsonable_encoder



router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)


@router.post("/post",  status_code=status.HTTP_201_CREATED)
def post_skills(response: Response, request: schemas.Skills,db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    new_skills = models.Skills(skill_type=request.skill_type,percentage=request.percentage,key_skill=request.key_skill)
    if not new_skills:
        response.staus_code = status.HTTP_501_NOT_IMPLEMENTED
    return crud.add_post(new_skills,db)



@router.get("/get", status_code=status.HTTP_202_ACCEPTED)
def get_skills(db:Session=Depends(crud.get_db)):
    return db.query(models.Skills).all()

@router.get("/get-{id}", status_code=status.HTTP_202_ACCEPTED)
def get_skills_by_id(id, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    skills_by_id = crud.queryDB_by_id(models.Skills,id,db).first()
    if not skills_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Skill with id={id} do not exist.")
    return skills_by_id

@router.delete("/delete-{id}", status_code=status.HTTP_202_ACCEPTED)
def del_skills_by_id(id, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    skill = crud.queryDB_by_id(models.Skills,id,db).delete(synchronize_session=False)
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The skill with id={id} do not exist.")
    db.commit()
    return {"Details":f"Skills with ID={id} is deleted."}



@router.put("/update-{id}", status_code=status.HTTP_202_ACCEPTED)
def update_skills_by_id(id,request: schemas.Skills, db:Session=Depends(crud.get_db), get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    skill = crud.queryDB_by_id(models.Skills,id,db).update(jsonable_encoder(request))
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The skill with id={id} do not exist.")
    db.commit()
    return {"Details":f"Skills with ID={id} is updated sucessfully."}