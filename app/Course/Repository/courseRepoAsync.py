from dataclasses import dataclass
from app.Course.Repository.courseRepositoryInterface import ICourseRepository
from app.models import Course
from app.schemas import CreateCourse, Course as CourseSchema
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional



@dataclass
class CourseRepositoryAsync(ICourseRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_course(self, course: CreateCourse) -> Course:
        new_course = Course(name=course.name, teacher_id=course.teacher_id)
        self.session.add(new_course)
        await self.session.commit()
        return new_course

    async def get_courses(self) -> List[CourseSchema]:
        result = await self.session.execute(select(Course))
        courses = [CourseSchema.from_orm(course) for course in result.scalars()]
        return courses
    
    async def get_course_by_name(self, name: str) -> Optional[CourseSchema]:
        result = await self.session.execute(
            select(Course).where(Course.name == name)
    )
        course = result.scalars().first()
        if course:
            return CourseSchema.from_orm(course)
        return None
    
    async def get_course_by_id(self, course_id: int) -> Optional[CourseSchema]:
        result = await self.session.execute(
            select(Course).where(Course.id == course_id)
        )
        course = result.scalars().first()
        if course:
            return CourseSchema.from_orm(course)
        return None
    
    async def delete_course_by_id(self, course_id: int) -> None:
        result = await self.session.execute(
            select(Course).where(Course.id == course_id)
        )
        course = result.scalars().first()
        if course:
            await self.session.delete(course)
            await self.session.commit()
        return
    
    async def get_course_by_name_and_teacher_id(self, course: CreateCourse) -> Optional[CourseSchema]:

        query  = select(Course).where(
            Course.name == course.name, 
            Course.teacher_id == course.teacher_id)

        result = await self.session.execute(query)

        course = result.scalars().first()

        if course:
            return CourseSchema.model_validate(course)
        return None

