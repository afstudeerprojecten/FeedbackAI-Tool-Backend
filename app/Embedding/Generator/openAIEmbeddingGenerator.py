


from dataclasses import dataclass

from fastapi import UploadFile

from app.Embedding.Generator.embeddingGeneratorInterface import IEmbeddingGenerator


@dataclass
class OpenAIEmbeddingGenerator(IEmbeddingGenerator):
    
    async def generateEmbeddings(self, file: UploadFile, out_):
        