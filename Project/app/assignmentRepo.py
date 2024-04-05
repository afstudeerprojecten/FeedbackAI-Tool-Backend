from dataclasses import dataclass
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Assignment as AssigntmentModel
from app.schemas import CreateAssignment as CreateAssignmentSchema
from app.schemas import Assignment as AssignmentSchema

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
        return new_assignment
    
    async def get_assignments(self) -> list[AssignmentSchema]:
        result = await self.session.execute(select(AssigntmentModel))
        result = await self.session.execute(select(AssigntmentModel).options(
                joinedload(AssigntmentModel.templates),
                joinedload(AssigntmentModel.course))
            )
        result = result.unique()
        assignments = [AssignmentSchema.model_validate(assignment) for assignment in result.scalars()]
        return assignments
    
    

    async def get_assignment_by_id(self, assignment_id: int) -> Optional[AssignmentSchema]:
        result = await self.session.execute(
            select (AssigntmentModel).where(AssigntmentModel.id == assignment_id)
        )
        assignment = result.scalars().first()
        if assignment:
            return AssignmentSchema.from_orm(assignment)
        return None
