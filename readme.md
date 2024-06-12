## Start with installing dependencies
```
pip install -r requirements.txt

```

## Run via
```
uvicorn app.main:app --reload
```


## Notes

### When updating models

[Read this!](https://fastapi.blog/blog/posts/2023-07-20-fastapi-sqlalchemy-migrations-guide/#step-6-generating-a-migration)

#### TL:DR

run this after updating models

```sh
docker run -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=feedbacktool -p 5432:5432 postgres
alembic upgrade head
alembic revision --autogenerate -m "Your message here"
alembic upgrade head
```


## Environment Variables
-  OPENAI_API_KEY variable
    An api key from OpenAI is needed to access their AI models.

- OPENAI_EMBEDDING_MODEL
    OpenAI's embedding model, such as "text-embedding-3-large"

- OPENAI_LANGUAGE_MODEL
    OpenAI's Large Languade Model, such as "gpt-4o"


- CHROMA_MODE variable, with one of the following values:
    - local, for when running Chroma locally on disk
    - remote, for when running Chroma as a HTTP client remotely<br>

    Add the following too:
    - CHROMA_PERSIST_DIRECTORY, in case it's ran locally, this is the folder where the database will be persisted
    - CHROMA_HOST, in case it's ran remote, must be the url the chroma HTTP client is run on
    - CHROMA_PORT, in case it's ran remote, must tbe the port the chroma HTTP client is runn on on CHROMA_HOST


- UPLOADED_FILES_FOLDER, this is the folder where uploaded files will be saved in case they're saved locally.

- OLLAMA_EMBEDDING_MODEL
    Ollama's embedding model that will be used when doing embeddings locally, for example "nomic-embed-text"
    Must have Ollama and the model installed on your computer.


### Deployment status

stable  
![status](https://argocd.iswleuven.be/api/badge?name=bp2024-stable&revision=true)

canary  
![status](https://argocd.iswleuven.be/api/badge?name=bp2024-qa&revision=true)