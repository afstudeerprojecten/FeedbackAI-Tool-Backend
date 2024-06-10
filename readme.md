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
alembic revision --autogenerate -m "Your message here"
alembic upgrade head
```


## Environment Variables
Create an OPENAI_API_KEY variable
An api key from OpenAI is needed to access their AI models.

Create a CHROMA_MODE variable, with one of the following values
local, for when running Chroma locally on disk
remote, for when running Chroma as a HTTP client remotely

CHROMA_HOST, in case it's ran remote, must be the url the chroma HTTP client is run on
CHROMA_PORT, in case it's ran remote, must tbe the port the chroma HTTP client is runn on on CHROMA_HOST