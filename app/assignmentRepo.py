from dataclasses import dataclass
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Assignment as AssigntmentModel
from app.schemas import CreateAssignment as CreateAssignmentSchema
from app.schemas import Assignment as AssignmentSchema
from app.schemas import AssignmentSimple as AssignmentSimpleSchema
from sqlalchemy.orm import joinedload

@dataclass
class AssignmentRepository:
    session: AsyncSession


    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_assignment(self, assignment: CreateAssignmentSchema) -> AssigntmentModel:
        new_assignment = AssigntmentModel(course_id=assignment.course_id, title=assignment.title, description=assignment.description, word_count=assignment.word_count, student_ages=assignment.student_ages)
        self.session.add(new_assignment)
        await self.session.commit()
        await self.session.refresh(new_assignment)
        new_assignment_validated = await self.get_assignment_by_id(new_assignment.id, eager_load=False)
        return new_assignment_validated
    
    async def get_assignments(self) -> list[AssignmentSchema]:
        result = await self.session.execute(select(AssigntmentModel).options(
                joinedload(AssigntmentModel.templates),
                joinedload(AssigntmentModel.course))
            )
        result = result.unique()
        assignments = [AssignmentSchema.model_validate(assignment) for assignment in result.scalars()]
        return assignments
    
    async def get_assignment_by_id(self, assignment_id: int, eager_load: bool=False) -> Optional[AssignmentSchema]:

        # If eager load, join with relationship attributes
        query = select(AssigntmentModel).where(AssigntmentModel.id == assignment_id)
        if eager_load:
            query = query.options(
                joinedload(AssigntmentModel.course)
            )
        
        # Always load templates... idk why doesn't work without
        query = query.options(joinedload(AssigntmentModel.templates))

        result = await self.session.execute(query)
        assignment = result.scalars().first()

        if assignment:
            # If not eager load, set relationship attributes explicitly to none, otherwise traceback errors
            if not eager_load:
                assignment.course = None
                assignment.templates = []
            return AssignmentSchema.model_validate(assignment)
        return None
    

    async def get_assignments_by_course_id(self, course_id: int) -> list[AssignmentSimpleSchema]:
        query = select(AssigntmentModel).where(AssigntmentModel.course_id == course_id)
        result = await self.session.execute(query)
        result = result.unique()
        assignments = [AssignmentSimpleSchema.model_validate(assignment) for assignment in result.scalars()]
        return assignments
        
    