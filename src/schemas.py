from pydantic import BaseModel
from typing import Optional



class User(BaseModel):
    nick_name: str
    email: str
    hashed_password: str
    is_active: bool
    class Config():
        orm_mode = True
class ShowUser(BaseModel): #to return just the email of the user (hidding ID and password)
    nick_name: str
    email: str
    class Config():
        orm_mode = True

class Education(BaseModel):
    ed_type: str
    ed_title: str
    ed_place: str
    website: str
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    active: bool
    class Config():
        orm_mode = True

class Skills(BaseModel):
    skill_type: str
    percentage: str
    key_skill: bool
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Projects(BaseModel):
    proj_name: str
    date_from: str
    date_to: str
    exp_id: int
    class Config():
        orm_mode = True

class Experience(BaseModel):
    date_from: str
    date_to: Optional[str] = None
    employer: str
    website: str
    job_description: str
    job_position: str

    class Config():
        orm_mode = True