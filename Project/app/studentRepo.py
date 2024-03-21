from dataclasses import dataclass    
import app.models as models
from sqlalchemy import Engine
from app.schemas import CreateStudent, Student
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Protocol, List


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class StudentRepositoryInterface(Protocol):
    def create_student(self, student: CreateStudent) -> models.Student:
        ...

@dataclass
class StudentRepository:
    engine: Engine
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
    def create_student(self, student: CreateStudent) -> models.Student:
        hashed_password = pwd_context.hash(student.password)
        with self.engine.connect() as conn:
            conn.execute(
                models.Student.__table__.insert().values(
                    name=student.name,
                    lastname=student.lastname,
                    email=student.email,
                    password=hashed_password,
                    organisation_id=student.organisation_id
            )
        )
        conn.commit()
        return models.Student(name=student.name, lastname=student.lastname, email=student.email, password=hashed_password, organisation_id=student.organisation_id)
    def get_students(self) -> List[Student]:
        with self.engine.connect() as conn:
            result = conn.execute(models.Student.__table__.select())
            students = []
            for row in result.fetchall():
                student_data = dict(row._asdict())
                student = student(**student_data)
                students.append(student)
            return students