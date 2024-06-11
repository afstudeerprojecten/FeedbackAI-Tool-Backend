from app.Embedding.Generator.embeddingGeneratorInterface import IEmbeddingGenerator
from dataclasses import dataclass
from fastapi import UploadFile
from langchain_openai import OpenAIEmbeddings
import os
from app.vector_database import OPENAI_EMBEDDING_MODEL_FALLBACK



@dataclass
class OpenAIEmbeddingGenerator(IEmbeddingGenerator):
    
    async def generateEmbeddings(self, file: UploadFile, out_):
        ... 

    def getEmbeddingFunction(self) -> str:
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", OPENAI_EMBEDDING_MODEL_FALLBACK))