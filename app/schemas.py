from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Command models for creating/updating data
class CreateOrganisation(BaseModel):
    name: str
    username: str
    password: str


class CreateAdmin(BaseModel):
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
    course_id: int
    teacher_id: int
    title: str
    description: str
    word_count: int
    student_ages: int


class CreateTemplate(BaseModel):
    assignment_id: int
    template_content: str

class CreateCourse(BaseModel):
    name: str
    teacher_id: int

class CreateSubmission(BaseModel):
    assignment_id: int
    student_id: int
    content: str

class CreateFeedback(BaseModel):
    submission_id: int
    content: str

class CreateEvent(BaseModel):
    name: str

class CreateEventLog(BaseModel):
    event_id: int
    user_id: int
    value: int

# Query models for retrieving data
class Organisation(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        orm_mode = True
        from_orm = True
        from_attributes=True

    
class Admin(BaseModel):
    id: int
    role: str
    username: str

    class Config:
        orm_mode = True
        from_orm = True
        from_attributes=True


class Teacher(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    organisation_id: int

    class Config:
        orm_mode = True
        from_attributes = True
        from_orm = True

class Student(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    organisation_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class Course(BaseModel):
    id: int
    name: str
    teacher_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class Assignment(BaseModel):
    id: int
    course_id: int
    title: str
    description: str
    word_count: int
    student_ages: int
    templates: Optional[List["Template"]] = []
    course: Optional[Course] = None

    class Config:
        orm_mode = True
        from_attributes = True

class AssignmentSimple(BaseModel):
    id: int
    course_id: int
    title: str
    description: str
    word_count: int
    student_ages: int

    class Config:
        orm_mode = True
        from_attributes = True


class Template(BaseModel):
    id: int
    content: str
    assignment_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class Submission(BaseModel):
    id: int
    content: str
    assignment_id: int
    student_id: int
    date_created: datetime
    assignment: Optional[Assignment] = Field(default=None)
    student: Optional[Student] = Field(default=None)
    feedback: Optional["Feedback"] = Field(default=None)

    class Config:
        orm_mode = True
        from_attributes = True

class SubmissionSimple(BaseModel):
    id: int
    content: str
    assignment_id: int
    student_id: int
    date_created: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class Feedback(BaseModel):
    id: int
    content: str
    submission_id: int

    class Config:
        orm_mode = True
        from_attributes = True

class Event(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        from_attributes = True

class EventLog(BaseModel):
    id :  int
    event_id : int
    user_id : int
    date_created : datetime
    value : int

    class Config:
        orm_mode = True
        from_attributes = True




#Update models
class UpdateTeacher(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    organisation_id: Optional[int] = None