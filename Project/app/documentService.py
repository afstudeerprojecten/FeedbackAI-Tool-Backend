import string
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles
import os
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import chromadb
from app.courseRepo import CourseRepository
from app.schemas import Course as CourseSchema, Organisation
from app.schemas import Organisation as OrganisationSchema
from app.teacherRepo import TeacherRepository
from app.vector_database import PERSISTENT_VECTOR_DB_FOLDER
from app.vector_database import OLLAMA_NOMIC_EMBEDDING
from app.vector_database import UPLOADED_FILES_FOLDER

class DocumentService:
    session: AsyncSession
    teacher_repo: TeacherRepository
    course_repo: CourseRepository

    def __init__(self, session: AsyncSession):
        self.session = session
        self.teacher_repo = TeacherRepository(session=session) 
        self.course_repo = CourseRepository(session=session)

    async def uploadDocument(
        self,  
        teacher_id: int,
        course_id: int,
        file: UploadFile ):


        # Get the course and organisation and teacher object
        teacher = await self.teacher_repo.get_teacher_by_id(teacher_id=teacher_id)
        course = await self.course_repo.get_course_by_id(course_id=course_id)
        organisation = await self.teacher_repo.get_organisation_by_teacher_id(teacher_id=teacher_id)

        # Save file locally
        out_file_path = await self.__saveFileLocally(file=file, organisation=organisation, course=course)

        # Make embeddings
        await self.__makeEmbeddings(file, out_file_path, organisation, course)

        return {"message": "file written out"}
    

    async def __saveFileLocally(self, file: UploadFile, organisation: Organisation, course: CourseSchema):
        #
        # OVerrides file if already exists for now, no validation yet
        # 

        
        # Uploaded files folder path
        uploaded_files_folder = UPLOADED_FILES_FOLDER
        # Create unique folder to save file to, using the organisation and course
        unique_course_folder_name = f"{organisation.name}_{organisation.id}_{course.name}_{course.id}/"
        # Final folder
        out_folder_path = os.path.join(uploaded_files_folder, unique_course_folder_name)
        print(out_folder_path)
        # Create the folder if it doesn't exist
        os.makedirs(out_folder_path, exist_ok=True)

        # Create the full file path
        out_file_path = os.path.join(out_folder_path, file.filename)
        # Save the file to the upload folder
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await file.read(1024):  # async read chunk
                await out_file.write(content)  # async write chunk

        return out_file_path
    
    
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
        loader = UnstructuredPDFLoader(file_path=out_file_path)
        data = loader.load()

        # print(data)

        # preview first page
        # print(data[0].page_content)

        # split the document into chunks, 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
        text_chunks = text_splitter.split_documents(data)

        ## Create persistent database directory to save vectors in 
        persistent_vector_db_directory = "./vector_database/"
        # Create the folder if it doesn't exist
        os.makedirs(persistent_vector_db_directory, exist_ok=True)
        
        # Create the embedding model
        ollama_nomic_embedding = OllamaEmbeddings(model="nomic-embed-text", show_progress=True)
        # embedding = OllamaEmbeddings(model="nomic-embed-text")
        
        # create the collection name, must be unique, so organization_course_
        organisation = await self.teacher_repo.get_organisation_by_teacher_id(teacher_id=teacher_id)

        course = await self.course_repo.get_course_by_id(course_id=course_id)

        unique_course_collection_name = f"{organisation.name}_{organisation.id}_{course.name}_{course.id}"

        print(unique_course_collection_name)

        # Persist to database
        vector_db = Chroma.from_documents(
            persist_directory=persistent_vector_db_directory,
            documents=text_chunks, 
            embedding=ollama_nomic_embedding,
            collection_name=unique_course_collection_name
        )

        vector_db.persist()

        vector_db = None

        ## Don't need this actually, just for test
        # Load from disk
        vector_db = Chroma(
            persist_directory=persistent_vector_db_directory,
            embedding_function=ollama_nomic_embedding,
            collection_name=unique_course_collection_name)
        
        # Print collection count
        print("There are", vector_db._collection.count(), "in the collection")

