import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb import chromadb
from chromadb import Settings
import shutil


PERSISTENT_VECTOR_DB_FOLDER  = "./vector_database/"


async def create_persistent_vector_db_folder():
    ## Create persistent database directory to save vectors in 
    folder = PERSISTENT_VECTOR_DB_FOLDER 
    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)


# Create the embedding model
OLLAMA_NOMIC_EMBEDDING = OllamaEmbeddings(model="nomic-embed-text", show_progress=True)


UPLOADED_FILES_FOLDER = "./uploaded_files/"



async def reset_vector_db():
    # settings = Settings(allow_reset=True)
    # vector_db = chromadb.PersistentClient(path=PERSISTENT_VECTOR_DB_FOLDER, settings=settings)
    # vector_db.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.
    shutil.rmtree(PERSISTENT_VECTOR_DB_FOLDER)
    print(f"{PERSISTENT_VECTOR_DB_FOLDER} and its contents deleted successfully.")
    # Create de folder dan nog
    await create_persistent_vector_db_folder()
    # print(f"{PERSISTENT_VECTOR_DB_FOLDER} does not exist.")