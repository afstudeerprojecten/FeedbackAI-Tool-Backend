from typing import Protocol

from fastapi import UploadFile

class IEmbeddingGenerator(Protocol):

    async def generateEmbeddings(self, file: UploadFile, out_):
        pass

