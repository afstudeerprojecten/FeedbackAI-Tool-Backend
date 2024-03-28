from dataclasses import dataclass
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Template as TemplateModel
from app.schemas import CreateAssignment as CreateAssignmentSchema
from app.schemas import CreateTemplate as CreateTemplateSchema
from app.schemas import Template as TemplateSchema


@dataclass
class TemplateRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_template(self, assignment_id: str, template_content: str) -> TemplateModel:
        new_template = TemplateModel(assigment_id=assignment_id, content=template_content)
        self.session.add(new_template)
        await self.session.commit()
        return new_template

    async def get_all_templates(self) -> list[TemplateSchema]:
        result = await self.session.execute(select(TemplateModel))
        templates = [TemplateSchema.model_validate(template) for template in result.scalars()]
        return templates