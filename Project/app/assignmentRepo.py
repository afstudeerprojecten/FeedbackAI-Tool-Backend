from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Assignment as AssigntmentModel
from app.schemas import CreateAssignment as CreateAssignmentSchema
from app.schemas import Assignment as AssignmentSchema


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
        assignments = [AssignmentSchema.model_validate(assignment) for assignment in result.scalars()]
        return assignments
