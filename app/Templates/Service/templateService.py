import os
import string
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.Templates.Repository.templateRepoAsync import TemplateRepositoryAsync
from app.Templates.Repository.templateRepositoryInterface import ITemplateRepository
from app.Templates.generator.templateGeneratorInterface import ITemplateGenerator
from app.Templates.generator.templateGeneratorOpenAI import TemplateGeneratorOpenAI
from app.Assignment.Repository.assignmentRepoAsync import AssignmentRepositoryAsync
from app.Course.Repository.courseRepoAsync import CourseRepositoryAsync
from dataclasses import dataclass
from typing import Self
from app.schemas import Template as TemplateSchema

@dataclass
class TemplateService:

    templateRepository: ITemplateRepository
    templateGenerator: ITemplateGenerator

    @classmethod
    def from_async_repo_and_open_ai_generator(cls, session: AsyncSession) -> Self:
        # maak hier de async repo aan
        # en de templategenerator
        templateRepository = TemplateRepositoryAsync(session)
        assignmentRepository = AssignmentRepositoryAsync(session)
        courseRepository= CourseRepositoryAsync(session=session)
        templateGenerator = TemplateGeneratorOpenAI(assignmentRepository=assignmentRepository, courseRepository=courseRepository)
        
        return TemplateService(templateRepository=templateRepository, templateGenerator=templateGenerator)
    
    async def generate_template_solution(self, assignment_id: int) -> str:
        return await self.templateGenerator.generate_template_solution(assignment_id=assignment_id)



    async def get_all_templates(self) -> list[TemplateSchema]:
        return await self.templateRepository.get_all_templates()
