from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from src.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nick_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    date_updated = Column(DateTime, default=datetime.now()) #this column will store current datetime by default, so we dont have to update this field during CRUD



class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    date_from = Column(String, index=True)
    date_to = Column(String, index=True)
    employer = Column(String, index=True)
    website = Column(String, index=True)
    job_description = Column(String, index=True)
    job_position = Column(String, index=True)
    active = Column(Boolean, index=True, default=True)
    date_updated = Column(DateTime, default=datetime.now()) #this column will store current datetime by default, so we dont have to update this field during CRUD


    projects = relationship("Projects", back_populates="exp")

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    ed_type = Column(String, index=True)
    ed_title = Column(String, index=True)
    ed_place = Column(String, index=True)
    website = Column(String, index=True)
    date_from = Column(String, index=True)
    date_to = Column(String, index=True)
    active = Column(Boolean, index=True, default=True)
    date_updated = Column(DateTime, default=datetime.now()) #this column will store current datetime by default, so we dont have to update this field during CRUD

class Skills(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    skill_type = Column(String, index=True)
    percentage = Column(Integer, index=True)
    key_skill = Column(Boolean, index=True)
    date_updated = Column(DateTime, default=datetime.now()) #this column will store current datetime by default, so we dont have to update this field during CRUD

class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    proj_name = Column(String, index=True)
    date_from = Column(String, index=True)
    date_to = Column(String, index=True)
    active = Column(Boolean, index=True, default=True)
    exp_id = Column(Integer, ForeignKey("experience.id"))

    exp = relationship("Experience", back_populates="projects")