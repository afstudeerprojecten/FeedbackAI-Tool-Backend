import os
import string
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.Assignment.Repository.assignmentRepositoryInterface import IAssignmentRepository
from app.Templates.Repository.templateRepoAsync import TemplateRepositoryAsync
from app.Templates.Repository.templateRepositoryInterface import ITemplateRepository
from app.Templates.generator.templateGeneratorInterface import ITemplateGenerator
from app.Templates.generator.templateGeneratorOpenAI import TemplateGeneratorOpenAI
from app.Assignment.Repository.assignmentRepoAsync import AssignmentRepositoryAsync
from app.Course.Repository.courseRepoAsync import CourseRepositoryAsync
from dataclasses import dataclass
from typing import Self
from app.exceptions import EntityNotFoundException
from app.schemas import Template as TemplateSchema
from app.schemas import CreateTemplate as CreateTemplateSchema
from app.models import Template as TemplateModel
from app.VectorDatabase.Repository.vectorDatabaseInterface import IVectorDatabase
from app.Embedding.Generator.openAIEmbeddingGenerator import OpenAIEmbeddingGenerator
from app.VectorDatabase.Repository.ChromaVectorDatabase import ChromaVectorDatabase

@dataclass
class TemplateService:

    templateRepository: ITemplateRepository
    templateGenerator: ITemplateGenerator
    assignmentRepository: IAssignmentRepository
    vectorDatabase: IVectorDatabase


    @classmethod
    def from_async_repo_and_open_ai_generator(cls, session: AsyncSession) -> Self:
        # maak hier de async repo aan
        # en de templategenerator
        templateRepository = TemplateRepositoryAsync(session)
        assignmentRepository = AssignmentRepositoryAsync(session)
        courseRepository= CourseRepositoryAsync(session=session)
        templateGenerator = TemplateGeneratorOpenAI(assignmentRepository=assignmentRepository, courseRepository=courseRepository)
        embeddingGenerator = OpenAIEmbeddingGenerator()
        vectorDatabase = ChromaVectorDatabase(embedding_generator=embeddingGenerator)
        
        return TemplateService(templateRepository=templateRepository, templateGenerator=templateGenerator, assignmentRepository=assignmentRepository, vectorDatabase=vectorDatabase)
    

    async def generate_template_solution(self, assignment_id: int) -> str:
        #check of assignment id echt is
        assignment = await self.assignmentRepository.get_assignment_by_id(assignment_id=assignment_id, eager_load=True)
        if (not assignment):
            raise EntityNotFoundException(message=f"Assignment with id {assignment_id} does not exist")
                # check of de course echt is
        course_id = await self.assignmentRepository.get_course_id_by_assignment_id(assignment_id=assignment.id)
        if (not course_id):
            raise EntityNotFoundException(message=f"Course with id {course_id} that assignment with id {assignment_id} belongs to doesn't exist.")
        
        # check of de organisation_id echt is
        organisation_id = await self.assignmentRepository.get_organisation_id_by_assignment_id(assignment_id=assignment_id)
        if (not organisation_id):
            raise EntityNotFoundException(message=f"Organisation with id {organisation_id} that this assignment with id {assignment_id} belongs to does not exist.")
        
        return await self.templateGenerator.generate_template_solution(assignment_id=assignment_id, vectorDatabase=self.vectorDatabase, organisation_id=organisation_id, course_id=course_id)


    async def get_all_templates(self) -> list[TemplateSchema]:
        return await self.templateRepository.get_all_templates()
    

    async def create_template(self, template: CreateTemplateSchema) -> TemplateModel:
        assignment = await self.assignmentRepository.get_assignment_by_id(template.assignment_id)
        if (not assignment):
            raise EntityNotFoundException(message=f"Assignment with id {template.assignment_id} does not exist")
        else:
            return await self.templateRepository.create_template(template=template)
    

    async def get_templates_for_assignment(self, assignment_id: int) -> list[TemplateSchema]:
        assignment = await self.assignmentRepository.get_assignment_by_id(assignment_id)
        if (not assignment):
            raise EntityNotFoundException(message=f"Assignment with id {assignment_id} does not exist")
        else:
            return await self.templateRepository.get_templates_for_assignment(assignment_id=assignment_id)