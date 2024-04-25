from dataclasses import dataclass
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.Templates.Repository.templateRepositoryInterface import ITemplateRepository
from app.models import Template as TemplateModel
from app.schemas import CreateAssignment as CreateAssignmentSchema
from app.schemas import CreateTemplate as CreateTemplateSchema
from app.schemas import Template as TemplateSchema


@dataclass
class TemplateRepositoryAsync(ITemplateRepository):
    session: AsyncSession

    async def create_template(self, template_content: CreateTemplateSchema) -> TemplateModel:
        new_template = TemplateModel(assignment_id=template_content.assignment_id, content=template_content.template_content)
        self.session.add(new_template)
        await self.session.commit()
        return new_template

    async def get_all_templates(self) -> list[TemplateSchema]:
        result = await self.session.execute(select(TemplateModel))
        templates = [TemplateSchema.model_validate(template) for template in result.scalars()]
        return templates

    async def get_templates_for_assignment(self, assignment_id: int) -> list[TemplateSchema]:
        result = await self.session.execute(
            select (TemplateModel).where(TemplateModel.assignment_id == assignment_id)
        )
        templates = [TemplateSchema.model_validate(template) for template in result.scalars()]
        return templates