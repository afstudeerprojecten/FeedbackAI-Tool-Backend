
from typing import Protocol

from app.VectorDatabase.Repository.vectorDatabaseInterface import IVectorDatabase

class ITemplateGenerator(Protocol):
    async def generate_template_solution(self, assignment_id: int, vectorDatabase: IVectorDatabase, organisation_id: int, course_id: int) -> str:
        ...