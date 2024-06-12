from typing import Protocol
from fastapi import UploadFile
from app.schemas import Course as CourseSchema, Organisation as OrganisationSchema
from langchain_core.vectorstores import VectorStoreRetriever

class IVectorDatabase(Protocol):

   # File_path is a str, meaning the path to the file
   # since depending on provider, the file_path can be a url or a local path 
   async def __checkEmbeddingAlreadyExists(self, file_path: str, organisation: OrganisationSchema, course: CourseSchema) -> bool:
       ...

        
   async def saveEmbeddings(self, file_path: str, organisation: OrganisationSchema, course: CourseSchema) -> None:
       ...

   def getUniqueCollectionName(self, organisation: OrganisationSchema, course: CourseSchema) -> str:
       ...

   def as_retriever(collection_name: str) -> VectorStoreRetriever:
       ...