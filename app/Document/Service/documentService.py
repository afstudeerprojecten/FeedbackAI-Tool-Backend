from dataclasses import dataclass
from re import S
import string
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles
import os
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import chromadb
from typing import Self
from app.Course.Repository.courseRepoAsync import CourseRepositoryAsync
from app.Course.Repository.courseRepositoryInterface import ICourseRepository
from app.Document.ObjectStore.objectStoreInterface import IObjectStore
from app.Document.ObjectStore.objectStoreLocalFileSystem import LocalFileSystemObjectStore
from app.Embedding.Generator.embeddingGeneratorInterface import IEmbeddingGenerator
from app.Embedding.Generator.nomicOllamaEmbeddingGenerator import NomicOllamaEmbeddingGenerator
from app.Teacher.Repository.teacherRepo import InterfaceTeacherRepository
from app.Teacher.Repository.teacherRepo import TeacherRepository as TeacherRepositoryAsync
from app.VectorDatabase.Repository.ChromaVectorDatabase import ChromaVectorDatabase
from app.VectorDatabase.Repository.vectorDatabaseInterface import IVectorDatabase
from app.schemas import Course as CourseSchema, Organisation
from app.schemas import Organisation as OrganisationSchema
from app.vector_database import PERSISTENT_VECTOR_DB_FOLDER
from app.vector_database import OLLAMA_NOMIC_EMBEDDING
from app.vector_database import UPLOADED_FILES_FOLDER

@dataclass
class DocumentService:


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
        unique_course_collection_name = f"{organisation.name}_{organisation.id}_{course.name}_{course.id}"

        ## Init een vector db met die collectie
        # collection_name doet get_or_create_collection al zelf, dus gaat altijd bestaan, ok... need to look inside the collection then 
        vector_db = Chroma(
            persist_directory=PERSISTENT_VECTOR_DB_FOLDER,
            embedding_function=OLLAMA_NOMIC_EMBEDDING,
            collection_name=unique_course_collection_name
            )

        # Location where the file is located in the file system, same as source metadata in vectordb
        # source_file_path = os.path.join(UPLOADED_FILES_FOLDER, unique_course_collection_name, file.filename)
        source_file_path = out_file_path

        # Else, Lees de collectie naam met extra info uit uit chroma db
        # met where source = feilname
        # en include metadata
        results = vector_db.get(
            where={"source": source_file_path},
            include=["metadatas"],
            )
        print(results)
        
        # dan als results > 0, dan bestaat die al... 
        if len(results["ids"]) > 0:
            print("Embedding for this file already exists")
            return True
        else:
            return False
      

    
    async def __makeEmbeddings(self, file: UploadFile, out_file_path: str, organisation: Organisation, course: CourseSchema):
         # Create the collection name, must be unique
        unique_course_collection_name = f"{organisation.name}_{organisation.id}_{course.name}_{course.id}"
        print(unique_course_collection_name)

        # Check if file already exists
        # If exists, skip creating embeddings
        if (await self.__checkEmbeddingAlreadyExists(file, out_file_path, organisation, course)):
            return "Embedding for this file already exists"
        
        #  Else continue creating embeddings

        # Load the file
        loader = UnstructuredPDFLoader(file_path=out_file_path)
        data = loader.load()

        # print(data)

        # preview first page
        # print(data[0].page_content)

        # split the document into chunks, 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
        text_chunks = text_splitter.split_documents(data)

        # Persist to database
        vector_db = Chroma.from_documents(
            persist_directory=PERSISTENT_VECTOR_DB_FOLDER,
            documents=text_chunks, 
            embedding=OLLAMA_NOMIC_EMBEDDING,
            collection_name=unique_course_collection_name
        )

        vector_db.persist()

        vector_db = None

        ## Don't need this actually, just for test
        # Load from disk
        vector_db = Chroma(
            persist_directory=PERSISTENT_VECTOR_DB_FOLDER,
            embedding_function=OLLAMA_NOMIC_EMBEDDING,
            collection_name=unique_course_collection_name)
        
        # Print collection count
        print("There are", vector_db._collection.count(), "in the collection")       