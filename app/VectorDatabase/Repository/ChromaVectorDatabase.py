from dataclasses import dataclass
import chromadb
from langchain_chroma import Chroma
from numpy import void
from app.Embedding.Generator.embeddingGeneratorInterface import IEmbeddingGenerator
from app.VectorDatabase.Repository.vectorDatabaseInterface import IVectorDatabase
from app.schemas import Course, Organisation
from app.schemas import Organisation as OrganisationSchema
from app.schemas import Course as CourseSchema
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.vector_database import PERSISTENT_VECTOR_DB_FOLDER
from app.vector_database import UPLOADED_FILES_FOLDER_FALLBACK
import os
from chromadb import HttpClient


@dataclass
class ChromaVectorDatabase(IVectorDatabase):

    embedding_generator: IEmbeddingGenerator
    chroma_mode = os.getenv("CHROMA_MODE", "local")
    chroma_host = os.getenv("CHROMA_HOST")
    chroma_port = os.getenv("CHROMA_PORT", "8000")
    chroma_persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./vector_database/")


    # moet een vectorstore initten... om daarin de embeds te bkijken... ja das letterlijk hierin ok 
    # tijdens check embeddings, 
    async def __checkEmbeddingAlreadyExists(self, file_path: str, organisation: OrganisationSchema, course: CourseSchema) -> bool:
        
        unique_course_collection_name: str = self.__getUniqueCollectionName(organisation=organisation, course=course)

        ## Init een vector db met die collectie
        # collection_name doet get_or_create_collection al zelf, dus gaat altijd bestaan, ok... need to look inside the collection then 
        vector_db = Chroma(
            persist_directory= self.chroma_persist_directory,
            embedding_function=self.embedding_generator.getEmbeddingFunction(),
            collection_name=unique_course_collection_name,
            client = self.__getChromaClient()
            )

        results = vector_db.get(
            where={"source": file_path},
            include=["metadatas"],
            )
        print(results)

        # If resultd > 0, means the embeddings already exist
        if len(results["ids"]) > 0:
            print("Embedding for this file already exists")
            return True
        else:
            return False

    # moet de embeddings generaten met zijn eigen embedding generator, en slaat die daaarna ook op 
    # moet 
    async def saveEmbeddings(self, file_path: str, organisation: OrganisationSchema, course: CourseSchema) -> void:
        # Create the collection name, must be unique
        unique_course_collection_name: str = self.__getUniqueCollectionName(organisation=organisation, course=course)
        print("unique course colleciton name for {organisation.name} and {course.name}" )
        print(unique_course_collection_name)

        # source_file_path = os.path.join(UPLOADED_FILES_FOLDER, unique_course_collection_name, file.filename)
        # Check if file already exists, If exists, skip creating embeddings
        if (await self.__checkEmbeddingAlreadyExists(file_path, organisation, course)):
            return "Embedding for this file already exists"

        # Else continue creating embeddings
        # Load the file
        loader = UnstructuredPDFLoader(file_path=file_path)
        data = loader.load()

        # print(data)
        # preview first page
        # print(data[0].page_content)

        # Split the document into chunks, 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
        text_chunks = text_splitter.split_documents(data)

        # Kan hier idd via openAI embeddings ook, moet gewoon via embeddingfunction
        # Persist to database
        vector_db = Chroma.from_documents(
            persist_directory= self.chroma_persist_directory,
            documents=text_chunks, 
            collection_name=unique_course_collection_name,
            embedding=self.embedding_generator.getEmbeddingFunction(),
            client = self.__getChromaClient()
        )

        vector_db.persist()

        vector_db = None

        ## Don't need this actually, just for test
        # Load from disk
        vector_db = Chroma(
            persist_directory=self.chroma_persist_directory,
            embedding_function=self.embedding_generator.getEmbeddingFunction(),
            collection_name=unique_course_collection_name)
        
        # Print collection count
        print("There are", vector_db._collection.count(), "in the collection")

    def __getUniqueCollectionName(self, organisation: OrganisationSchema, course: CourseSchema) -> str:
        return f"{organisation.id}_{course.id}"
    
    def __getChromaClient(self):
        if self.chroma_mode == "local":
            chroma_client = None
        elif self.chroma_mode == "remote":
            if self.chroma_host == None:
                # fallback to same as chroma_mode = local again...
                chroma_client = None
            else:
                chroma_client = HttpClient(
                    host = self.chroma_host,
                    port = self.chroma_port
                )
        else:
            raise ValueError(f"Invalid CHROMA_MODE: {self.chroma_mode}.\nPlease refer to the readme.")
        
        return chroma_client