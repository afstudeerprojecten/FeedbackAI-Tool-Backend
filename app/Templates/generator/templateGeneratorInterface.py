
from typing import Protocol

class ITemplateGenerator(Protocol):
    async def generate_template_solution(self, assignment_id: int) -> str:
        ...