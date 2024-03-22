from dataclasses import dataclass
from app.models import Organisation
from app.schemas import CreateOrganisation
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class OrganisationRepository:
    session: AsyncSession
    
    async def create_organisation(self, organisation: CreateOrganisation) -> Organisation:
        hashed_password = pwd_context.hash(organisation.password)
        async with self.session() as session:
            async with session.begin():
                await session.execute(
                    Organisation.__table__.insert().values(
                        name=organisation.name,
                        username=organisation.username,
                        password=hashed_password
                    )
                )
            await session.commit()
        return Organisation(name=organisation.name, username=organisation.username, password=hashed_password)
    
    async def get_organisations(self) -> List[Organisation]:
        async with self.session() as session:
            result = await session.execute(select(Organisation))
            organisations = [Organisation(**row) for row in result.scalars()]
            return organisations
        
    async def get_organisation_by_name(self, name: str) -> Organisation:
        async with self.session() as session:
            result = await session.execute(
                select(Organisation).where(Organisation.name == name)
            )
            return await result.fetchone()