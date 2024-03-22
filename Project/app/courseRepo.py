# from dataclasses import dataclass
# import app.models as models
# from sqlalchemy import Engine
# from app.schemas import CreateCourse, Course
# from sqlalchemy.orm import Session
# from passlib.context import CryptContext
# from typing import Protocol, List



# class CourseRepositoryInterface(Protocol):
#     def create_course(self, course: CreateCourse) -> models.Course:
#         ...


# @dataclass
# class CourseRepository:
#     engine: Engine
#     def __init__(self, engine: Engine) -> None:
#         self.engine = engine
#     def create_course(self, course: CreateCourse) -> models.Course:
#         with self.engine.connect() as conn:
#             conn.execute(
#                 models.Course.__table__.insert().values(
#                     name=course.name,
#                     teacher_id=course.teacher_id
#             )
#         )
#         conn.commit()
#         return models.Course(name=course.name, teacher_id=course.teacher_id)
#     def get_courses(self) -> List[Course]:
#         with self.engine.connect() as conn:
#             result = conn.execute(models.Course.__table__.select())
#             courses = []
#             for row in result.fetchall():
#                 course_data = dict(row._asdict())
#                 course = Course(**course_data)
#                 courses.append(course)
#             return courses