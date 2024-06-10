from dataclasses import dataclass
from re import S
import string
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles
import os
import chromadb
from typing import Self

from torch import embedding
from app.Course.Repository.courseRepoAsync import CourseRepositoryAsync
from app.Course.Repository.courseRepositoryInterface import ICourseRepository
from app.Document.ObjectStore.objectStoreInterface import IObjectStore
from app.Document.ObjectStore.objectStoreLocalFileSystem import LocalFileSystemObjectStore
from app.Embedding.Generator.embeddingGeneratorInterface import IEmbeddingGenerator
from app.Embedding.Generator.nomicOllamaEmbeddingGenerator import NomicOllamaEmbeddingGenerator
from app.Embedding.Generator.openAIEmbeddingGenerator import OpenAIEmbeddingGenerator
from app.Teacher.Repository.teacherRepo import InterfaceTeacherRepository
from app.Teacher.Repository.teacherRepo import TeacherRepository as TeacherRepositoryAsync
from app.VectorDatabase.Repository.ChromaVectorDatabase import ChromaVectorDatabase
from app.VectorDatabase.Repository.vectorDatabaseInterface import IVectorDatabase
from app.schemas import Course as CourseSchema, Organisation
from app.schemas import Organisation as OrganisationSchema

@dataclass
class DocumentService:
    # doc service needs
    # async session, file saver, embedding generator, vector store, 
    # opslaan in aparte mappen? 
        # dan file saver hier enkel, embedding generator hier enkel, en vector store heb op meerdere plekken nodig, wa kan daarin? vb de save files voor persist, en maken ervan vb voor de init, ja... 
    teacher_repo: InterfaceTeacherRepository
    course_repo: ICourseRepository
    object_store: IObjectStore
    embedding_generator: IEmbeddingGenerator
    vector_database: IVectorDatabase


    @classmethod
    def from_async_repos_and_local_files_and_nomic_embed_and_chroma_local(cls, session: AsyncSession) -> Self:
        teacher_repo = TeacherRepositoryAsync(session=session)
        course_repo = CourseRepositoryAsync(session=session)
        object_store = LocalFileSystemObjectStore()
        embedding_generator = NomicOllamaEmbeddingGenerator()
        vector_database = ChromaVectorDatabase(embedding_generator=embedding_generator)

        return DocumentService(teacher_repo=teacher_repo, course_repo=course_repo, object_store=object_store, embedding_generator=embedding_generator, vector_database=vector_database)


    # def __init__(self, session: AsyncSession):
    #     self.session = session
    #     self.teacher_repo = TeacherRepositoryAsync(session=session) 
    #     self.course_repo = CourseRepositoryAsync(session=session)

    async def uploadDocument(
        self,  
        teacher_id: int,
        course_id: int,
        file: UploadFile ):
        
        # Get the teacher , course and organisation object
        teacher = await self.teacher_repo.get_teacher_by_id(teacher_id=teacher_id)
        course = await self.course_repo.get_course_by_id(course_id=course_id)
        organisation = await self.teacher_repo.get_organisation_by_teacher_id(teacher_id=teacher_id)

        # Save file locally
        out_file_path = await self.object_store.saveFile(file=file, organisation=organisation, course=course)

        # await self.__makeEmbeddings(file, out_file_path, organisation, course)

        # sla de embeddings op
        # deze maakt de embeddings ook, en generate 
        # embeddinggenerator meegeven, en de file
        # want moet via db doen want die gaat ookkkk checken op voorhand al of da is, ok.. dus ok? s

        # await self.vector_database.save_embeddings(embeddinggenerator meegeven, de file, )
        await self.vector_database.saveEmbeddings(out_file_path, organisation=organisation, course=course)

        # Make embeddings
        await self.embedding_generator.generate_embeddings()

        return {"message": "file written out"}    
    
    async def __checkEmbeddingAlreadyExists(self, file: UploadFile, out_file_path: str, organisation: Organisation, course: CourseSchema):
        pass
      

    
    async def __makeEmbeddings(self, file: UploadFile, out_file_path: str, organisation: Organisation, course: CourseSchema):
        pass
       