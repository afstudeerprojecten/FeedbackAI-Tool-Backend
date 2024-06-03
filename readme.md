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