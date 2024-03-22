# from dataclasses import dataclass    
# import app.models as models
# from sqlalchemy import create_engine
# from app.schemas import CreateTeacher, Teacher
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from passlib.context import CryptContext
# from typing import Protocol, List


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class TeacherRepositoryInterface(Protocol):
#     async def create_teacher(self, teacher: CreateTeacher) -> models.Teacher:
#         ...

# @dataclass
# class TeacherRepository:
#     engine: create_async_engine

#     async def create_teacher(self, teacher: CreateTeacher) -> models.Teacher:
#         hashed_password = pwd_context.hash(teacher.password)
#         async with self.engine.begin() as conn:
#             await conn.execute(
#                 models.Teacher.__table__.insert().values(
#                     name=teacher.name,
#                     lastname=teacher.lastname,
#                     email=teacher.email,
#                     password=hashed_password,
#                     organisation_id=teacher.organisation_id
#                 )
#             )
#         return models.Teacher(name=teacher.name, lastname=teacher.lastname, email=teacher.email, password=hashed_password, organisation_id=teacher.organisation_id)

#     async def get_teachers(self) -> List[Teacher]:
#         async with self.engine.begin() as conn:
#             result = await conn.execute(models.Teacher.__table__.select())
#             teachers = []
#             async for row in result:
#                 teacher_data = dict(row.items())
#                 teacher = Teacher(**teacher_data)
#                 teachers.append(teacher)
#             return teachers
