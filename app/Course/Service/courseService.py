from dataclasses import dataclass
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Self
from app.Course.Repository.courseRepoAsync import CourseRepositoryAsync
from app.Course.Repository.courseRepositoryInterface import ICourseRepository
from app.exceptions import EntityNotFoundException, EntityValidationException
from app.schemas import CreateCourse, Course as CourseSchema
from typing import List, Optional
from app.models import Course

@dataclass
class CourseService:
    
    courseRepository: ICourseRepository

    @classmethod
    def from_async_repo(cls, session: AsyncSession) -> Self:
        courseRepository = CourseRepositoryAsync(session)
        return CourseService(courseRepository=courseRepository)
    
    async def create_course(self, course: CreateCourse) -> Course:

        # Check of er al een course met deze name en teacher id bestaan in de repo, 
        # if so return error unique combo already exists, ok 
        if await self.courseRepository.get_course_by_name_and_teacher_id(course=course):
            raise EntityValidationException(f"Course with this name {course.name} and teacher_id {course.teacher_id} combination already exists")
        return await self.courseRepository.create_course(course=course)

    async def get_courses(self) -> List[CourseSchema]:
        return await self.courseRepository.get_courses()
    
    async def get_course_by_name(self, name: str) -> Optional[CourseSchema]:
        
        course = await self.courseRepository.get_course_by_name(name=name)
        if (not course):
            raise EntityNotFoundException(message=f"Course with name {name} does not exist")
        else:
            return course
    
    async def get_course_by_id(self, course_id: int) -> Optional[CourseSchema]:
        course = await self.courseRepository.get_course_by_id(course_id=course_id)
        if (not course):
            raise EntityNotFoundException(message=f"Course with id {course_id} does not exist")
        else:
            return course

    
    async def delete_course_by_id(self, course_id: int) -> None:
        if (not await self.courseRepository.get_course_by_id(course_id=course_id)):
            raise EntityNotFoundException(message=f"Course with id {course_id} does not exist")
        else:
            return await self.courseRepository.delete_course_by_id(course_id=course_id)
