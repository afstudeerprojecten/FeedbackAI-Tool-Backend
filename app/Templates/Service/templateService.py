import os
import string
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.Templates.Repository.templateRepo import TemplateRepositoryAsync
from app.Templates.Repository.templateRepositoryInterface import ITemplateRepository
from app.Templates.generator.templateGeneratorInterface import ITemplateGenerator
from app.Templates.generator.templateGeneratorOpenAI import TemplateGeneratorOpenAI
from app.assignmentRepo import AssignmentRepository
from app.courseRepo import CourseRepository
from dataclasses import dataclass
from typing import Self

@dataclass
class TemplateService:

    session: AsyncSession
    templateRepository: ITemplateRepository
    templateGenerator: ITemplateGenerator
    
    async def generate_template_solution(self, assignment_id: int) -> str:
        return await self.templateGenerator.generate_template_solution(assignment_id=assignment_id)


    @classmethod
    def from_async_repo_and_open_ai_generator(cls, session: AsyncSession) -> Self:
        # maak hier de async repo aan
        # en de templategenerator
        templateRepository = TemplateRepositoryAsync(session)
        templateGenerator = TemplateGeneratorOpenAI()

        return TemplateService(session=session, templateRepository=templateRepository, templateGenerator=templateGenerator)
