from dataclasses import dataclass
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Self
from app.Course.Repository.courseRepoAsync import CourseRepositoryAsync
from app.Course.Repository.courseRepositoryInterface import ICourseRepository
from app.schemas import CreateCourse, Course as CourseSchema
from typing import List, Optional
from app.models import Course



class UniqueCourseNameAndTeacherIdCombinationExcepton(Exception):
    def __init__(self, course: CreateCourse):
        self.course = course

async def unique_course_name_and_teacher_id_combination_exception_handler(request, e: UniqueCourseNameAndTeacherIdCombinationExcepton):
    return JSONResponse(
        status_code=409,
        content={"message": f"Course with this name {e.course.name} and teacher_id {e.course.teacher_id} combination already exists"}
    )

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
            raise UniqueCourseNameAndTeacherIdCombinationExcepton(course=course)
        return await self.courseRepository.create_course(course=course)

    async def get_courses(self) -> List[CourseSchema]:
        return await self.courseRepository.get_courses()
    
    async def get_course_by_name(self, name: str) -> Optional[CourseSchema]:
        return await self.courseRepository.get_course_by_name(name=name)
    
    async def get_course_by_id(self, course_id: int) -> Optional[CourseSchema]:
        return await self.courseRepository.get_course_by_id(course_id=course_id)
    
    async def delete_course_by_id(self, course_id: int) -> None:
        return await self.courseRepository.delete_course_by_id(course_id=course_id)
