from dataclasses import dataclass    
import app.models as models
from sqlalchemy import Engine
from app.schemas import CreateTeacher
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Protocol


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TeacherRepositoryInterface(Protocol):
    def create_teacher(self, teacher: CreateTeacher) -> models.Teacher:
        ...

@dataclass
class TeacherRepository:
    engine: Engine
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
    def create_teacher(self, teacher: CreateTeacher) -> models.Teacher:
        hashed_password = pwd_context.hash(teacher.password)
        with self.engine.connect() as conn:
            conn.execute(
                models.Teacher.__table__.insert().values(
                    name=teacher.name,
                    lastname=teacher.lastname,
                    email=teacher.email,
                    password=hashed_password,
                    organisation_id=teacher.organisation_id
            )
        )
        conn.commit()
        return models.Teacher(name=teacher.name, lastname=teacher.lastname, email=teacher.email, password=hashed_password, organisation_id=teacher.organisation_id)

    def get_teachers(self) -> models.Teacher:
        with self.engine.connect() as conn:
            result = conn.execute(
                models.Teacher.__table__.select()
            )
            return result.fetchall()