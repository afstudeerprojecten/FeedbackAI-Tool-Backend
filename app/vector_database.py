import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import shutil

PERSISTENT_VECTOR_DB_FOLDER  = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/persistent_vector_db/")

# Dit is enkel nodig voor chromadb lokaal? 
async def create_persistent_vector_db_folder():
    print(PERSISTENT_VECTOR_DB_FOLDER)
    ## Create persistent database directory to save vectors in. Defaults ./data/persistent_vector_db/   
    folder = PERSISTENT_VECTOR_DB_FOLDER
    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

# Create the embedding model
OLLAMA_NOMIC_EMBEDDING = OllamaEmbeddings(model="nomic-embed-text", show_progress=True)

UPLOADED_FILES_FOLDER_FALLBACK = "./data/uploaded_files/"

OPENAI_EMBEDDING_MODEL_FALLBACK = "text-embedding-3-large"

async def reset_vector_db():
    # settings = Settings(allow_reset=True)
    # vector_db = chromadb.PersistentClient(path=PERSISTENT_VECTOR_DB_FOLDER, settings=settings)
    # vector_db.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.
    shutil.rmtree(PERSISTENT_VECTOR_DB_FOLDER)
    print(f"{PERSISTENT_VECTOR_DB_FOLDER} and its contents deleted successfully.")
    # Create de folder dan nog
    await create_persistent_vector_db_folder()
    # print(f"{PERSISTENT_VECTOR_DB_FOLDER} does not exist.")