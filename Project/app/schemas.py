from pydantic import BaseModel
from typing import Optional, List


# Command models for creating/updating data
class CreateOrganisation(BaseModel):
    name: str
    username: str
    password: str


class CreateTeacher(BaseModel):
    name: str
    lastname: str
    email: str
    password: str
    organisation_id: int


class CreateStudent(BaseModel):
    name: str
    lastname: str
    email: str
    password: str
    organisation_id: int


class CreateAssignment(BaseModel):
    name: str
    teacher_id: int
    template_contents: List[str]


class CreateTemplate(BaseModel):
    assignment_id: int
    template_content: str


# Query models for retrieving data
class Organisation(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        orm_mode = True


class Teacher(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    password: str
    organisation_id: int

    class Config:
        orm_mode = True


class Student(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    password: str
    organisation_id: int

    class Config:
        orm_mode = True


class Course(BaseModel):
    id: int
    name: str
    teacher_id: int

    class Config:
        orm_mode = True


class Assignment(BaseModel):
    id: int
    name: str
    teacher_id: int
    templates: List["Template"] = []

    class Config:
        orm_mode = True


class Template(BaseModel):
    id: int
    content: str
    assignment_id: int

    class Config:
        orm_mode = True


class Submission(BaseModel):
    id: int
    content: str
    assignment_id: int
    student_id: int

    class Config:
        orm_mode = True


class Feedback(BaseModel):
    id: int
    content: str
    submission_id: int

    class Config:
        orm_mode = True
