from typing import Optional
from app.models import Assignment as AssigntmentModel
from app.schemas import CreateAssignment as CreateAssignmentSchema
from app.schemas import Assignment as AssignmentSchema
from app.schemas import AssignmentSimple as AssignmentSimpleSchema
from typing import Protocol


class IAssignmentRepository(Protocol):
    async def create_assignment(self, assignment: CreateAssignmentSchema) -> AssigntmentModel:
        ...
    
    async def get_assignments(self) -> list[AssignmentSchema]:
        ...
    
    async def get_assignment_by_id(self, assignment_id: int, eager_load: bool=True) -> Optional[AssignmentSchema]:
        ...
    

    async def get_assignments_by_course_id(self, course_id: int) -> list[AssignmentSimpleSchema]:
        ...
        
    async def get_assignment_by_title_and_course_id(self, assignment: CreateAssignmentSchema) -> AssigntmentModel:
        ...

    async def get_course_id_by_assignment_id(self, assignment_id: int) -> Optional[int]:
        ...

    async def get_organisation_id_by_assignment_id(self, assignment_id: int) -> Optional[int]:
        ...
