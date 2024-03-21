from typing import Protocol
from fastapi import FastAPI, HTTPException, Depends, status
from enum import Enum
from sqlalchemy import Engine
from sqlalchemy.orm import Session
import os
from jose import jwt
from dataclasses import dataclass    
import app.models as models
from app.database import engine, SessionLocal
from app.organisationRepo import OrganisationRepository
from app.studentRepo import StudentRepository
from app.teacherRepo import TeacherRepository
from app.adminRepo import AdminRepository
from app.schemas import Organisation, Teacher, CreateOrganisation, CreateTeacher, CreateStudent, Student, CreateAdmin, Admin

app = FastAPI()
models.Base.metadata.create_all(bind=engine)



@dataclass
class APIResponse:
    data: dict
    status: int = 200




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# No need for db_dependency annotation
def db_dependency():
    return Depends(get_db)


@app.get("/")
async def root():
    return {"message": "Welcome to the API, made with FastAPI!!"}


#ADMIN
# Middleware to create superuser if Admin table is empty
def create_superuser_if_empty(db: Session):
    admin_repo = AdminRepository(engine)
    admin_count = admin_repo.get_admins_count()
    if admin_count == 0:
        # Add your superuser details here
        superuser = CreateAdmin(username="admin", password="adminpassword")
        admin_repo.create_admin(superuser)
# Middleware to create superuser if Admin table is empty
@app.middleware("http")
async def create_superuser_middleware(request, call_next, db: Session = Depends(get_db)):
    create_superuser_if_empty(db)
    response = await call_next(request)
    return response

#ORGANISATION

@app.post("/organisation/add")
async def create_organisation(organisation: CreateOrganisation):
    try:
        repo = OrganisationRepository(engine)
        repo.create_organisation(organisation)
        return {"message": "Organisation created successfully"}
    except Exception as e:
        # Log the error if needed
        # logger.error("An error occurred while creating an item: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/organisations")
async def get_organisations():
    try:
        repo = OrganisationRepository(engine)
        organisations = repo.get_organisations()
        return APIResponse(data=organisations)
    except Exception as e:
        # Log the error if needed
        # logger.error("An error occurred while creating an item: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

#TEACHER
@app.post("/teacher/add")
async def create_teacher(teacher: CreateTeacher):
    try:
        repo = TeacherRepository(engine)
        repo.create_teacher(teacher)
        return {"message": "Teacher created successfully"}
    except Exception as e:
        # Log the error if needed
        # logger.error("An error occurred while creating an item: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/teachers")
async def get_teachers():
    try:
        repo = TeacherRepository(engine)
        teachers = repo.get_teachers()
        return APIResponse(data=teachers)
    except Exception as e:
        # Log the error if needed
        # logger.error("An error occurred while creating an item: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    
#STUDENT
@app.post("/student/add")
async def create_student(student: CreateStudent):
    try:
        repo = StudentRepository(engine)
        repo.create_student(student)
        return {"message": "Student created successfully"}
    except Exception as e:
        # Log the error if needed
        # logger.error("An error occurred while creating an item: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/students")
async def get_students():
    try:
        repo = StudentRepository(engine)
        students = repo.get_students()
        return APIResponse(data=students)
    except Exception as e:
        # Log the error if needed
        # logger.error("An error occurred while creating an item: %s", e)
        raise HTTPException(status_code=500, detail=str(e))