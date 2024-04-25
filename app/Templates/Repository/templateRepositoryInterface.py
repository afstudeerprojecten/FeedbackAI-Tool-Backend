from typing import Protocol
from dataclasses import dataclass
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Template as TemplateModel
from app.schemas import CreateAssignment as CreateAssignmentSchema
from app.schemas import CreateTemplate as CreateTemplateSchema
from app.schemas import Template as TemplateSchema

class ITemplateRepository(Protocol):
    async def create_template(self, template_content: CreateTemplateSchema) -> TemplateModel:
        ...

    async def get_all_templates(self) -> list[TemplateSchema]:
        ...


    async def get_templates_for_assignment(self, assignment_id: int) -> list[TemplateSchema]:
        ...