from app.models import Course
from app.schemas import CreateCourse, Course as CourseSchema
from typing import List, Optional, Protocol


class ICourseRepository(Protocol):
    async def create_course(self, course: CreateCourse) -> Course:
        ...

    async def get_courses(self) -> List[CourseSchema]:
        ...
    
    async def get_course_by_name(self, name: str) -> Optional[CourseSchema]:
        ...
    
    async def get_course_by_id(self, course_id: int) -> Optional[CourseSchema]:
        ...
    
    async def delete_course_by_id(self, course_id: int) -> None:
        ...

    async def get_course_by_name_and_teacher_id(self, course: CreateCourse) -> Optional[CourseSchema]:
        ...