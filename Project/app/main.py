# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_engine, SessionLocal as async_session
from app.organisationRepo import OrganisationRepository
from app.schemas import Organisation, CreateOrganisation
import asyncio
from app.models import Base

app = FastAPI()


async def get_async_db():
    async with async_session() as session:
        yield session


# No need for db_dependency annotation
def db_dependency():
    return Depends(get_async_db)


@app.get("/")
async def root():
    return {"message": "Welcome to the API, made with FastAPI!!"}


# ORGANISATION
@app.post("/organisation/add")
async def create_organisation(organisation: CreateOrganisation, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = OrganisationRepository(db)
        await repo.create_organisation(organisation)
        return {"message": "Organisation created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/organisations")
async def get_organisations(db: AsyncSession = Depends(get_async_db)):
    try:
        repo = OrganisationRepository(db)
        organisations = await repo.get_organisations()
        return organisations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def startup_event():
    await create_tables()
    await asyncio.sleep(5)  # Wait for tables to be created before starting the application

# Register the startup event
app.add_event_handler("startup", startup_event)

# Note: No need for the if __name__ == "__main__": block
