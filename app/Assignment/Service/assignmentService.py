from dataclasses import dataclass
from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession
from app.Assignment.Repository.assignmentRepoAsync import AssignmentRepositoryAsync
from app.Assignment.Repository.assignmentRepositoryInterface import IAssignmentRepository
from typing import Optional
from app.models import Assignment as AssigntmentModel
from app.schemas import CreateAssignment as CreateAssignmentSchema
from app.schemas import Assignment as AssignmentSchema
from app.schemas import AssignmentSimple as AssignmentSimpleSchema
from typing import Protocol

@dataclass
class AssignmentService:
    assignmentRepository: IAssignmentRepository

    @classmethod
    def from_async_repo(cls, session: AsyncSession) -> Self:
        assignmentRepository = AssignmentRepositoryAsync(session)
        return AssignmentService(assignmentRepository=assignmentRepository)


    async def create_assignment(self, assignment: CreateAssignmentSchema) -> AssigntmentModel:
        return await self.assignmentRepository.create_assignment(assignment=assignment)
    
    async def get_assignments(self) -> list[AssignmentSchema]:
        return await self.assignmentRepository.get_assignments()
    
    async def get_assignment_by_id(self, assignment_id: int, eager_load: bool=False) -> Optional[AssignmentSchema]:
        return await self.assignmentRepository.get_assignment_by_id(assignment_id=assignment_id, eager_load=eager_load)
    

    async def get_assignments_by_course_id(self, course_id: int) -> list[AssignmentSimpleSchema]:
        return await self.assignmentRepository.get_assignments_by_course_id(course_id=course_id)