from dataclasses import dataclass
from fastapi import UploadFile
from app.Embedding.Generator.embeddingGeneratorInterface import IEmbeddingGenerator
from langchain_community.embeddings import OllamaEmbeddings


@dataclass

class NomicOllamaEmbeddingGenerator(IEmbeddingGenerator):


    # heeft toegang nodig tot de vectordatabase.... waarom opdelen? teveel opgedeeld tbf...? 
    # heb file loader nodig... 
    # ipv file mee te geven, mss gewoon al inladen via een loader, en dan de data meegeven gewoon ok 
    # 
    async def generateEmbeddings(self, file: UploadFile, out_):
        return await super().makeEmbeddings(file, out_)()
    
