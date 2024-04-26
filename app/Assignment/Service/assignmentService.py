from dataclasses import dataclass
from typing import Self
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.Assignment.Repository.assignmentRepoAsync import AssignmentRepositoryAsync
from app.Assignment.Repository.assignmentRepositoryInterface import IAssignmentRepository
from typing import Optional
from app.models import Assignment as AssigntmentModel
from app.schemas import CreateAssignment as CreateAssignmentSchema
from app.schemas import Assignment as AssignmentSchema
from app.schemas import AssignmentSimple as AssignmentSimpleSchema
from typing import Protocol

class UniqueAssignmentTitlePerCourseException(Exception):
    def __init__(self, assignment: CreateAssignmentSchema):
        self.assigment = assignment

async def unique_assignment_title_per_course_id_combination_exception_handler(request, e: UniqueAssignmentTitlePerCourseException):
    return JSONResponse(
        status_code=409,
        content={"message": f"Assignment with this title {e.assigment.title} for the course with course_id {e.assigment.course_id} already exists. Assignment title must be unique per course"}
    )

@dataclass
class AssignmentService:
    assignmentRepository: IAssignmentRepository

    @classmethod
    def from_async_repo(cls, session: AsyncSession) -> Self:
        assignmentRepository = AssignmentRepositoryAsync(session)
        return AssignmentService(assignmentRepository=assignmentRepository)


    async def create_assignment(self, assignment: CreateAssignmentSchema) -> AssigntmentModel:
        
        assignmentExists =  await self.assignmentRepository.get_assignment_by_title_and_course_id(assignment=assignment)
        
        if (assignmentExists):
            raise UniqueAssignmentTitlePerCourseException(assignment=assignment)
        return await self.assignmentRepository.create_assignment(assignment=assignment)
    
    async def get_assignments(self) -> list[AssignmentSchema]:
        return await self.assignmentRepository.get_assignments()
    
    async def get_assignment_by_id(self, assignment_id: int, eager_load: bool=False) -> Optional[AssignmentSchema]:
        return await self.assignmentRepository.get_assignment_by_id(assignment_id=assignment_id, eager_load=eager_load)
    

    async def get_assignments_by_course_id(self, course_id: int) -> list[AssignmentSimpleSchema]:
        return await self.assignmentRepository.get_assignments_by_course_id(course_id=course_id)