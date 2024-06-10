from dataclasses import dataclass
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
from app.vector_database import OLLAMA_NOMIC_EMBEDDING
from app.vector_database import UPLOADED_FILES_FOLDER
import os


@dataclass
class ChromaVectorDatabase(IVectorDatabase):

    embedding_generator: IEmbeddingGenerator
    chroma_mode = os.getenv("CHROMA_MODE", "local")

# moet een vectorstore initten... om daarin de embeds te bkijken... ja das letterlijk hierin ok 
# tijdens check embeddings, 
    async def __checkEmbeddingAlreadyExists(self, file_path: str, organisation: Organisation, course: Course) -> bool:
    # moet de embeddings generaten met zijn eigen embedding generator, en slaat die daaarna ook op 
    # moet 
    async def saveEmbeddings(self, file_path: str, organisation: OrganisationSchema, course: CourseSchema) -> void:
