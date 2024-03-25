from dataclasses import dataclass
from app.models import Organisation
from app.schemas import CreateOrganisation, Organisation as OrganisationSchema
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class OrganisationRepository:
    session: AsyncSession
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_organisation(self, organisation: CreateOrganisation) -> Organisation:
        hashed_password = pwd_context.hash(organisation.password)
        new_organisation = Organisation(name=organisation.name, username=organisation.username, password=hashed_password)
        self.session.add(new_organisation)
        await self.session.commit()
        return new_organisation
    
    async def get_organisations(self) -> List[OrganisationSchema]:
        result = await self.session.execute(select(Organisation))
        organisations = [OrganisationSchema.from_orm(org) for org in result.scalars()]
        return organisations
        
    async def get_organisation_by_name(self, name: str) -> Organisation:
        async with self.session() as session:
            result = await session.execute(
                select(Organisation).where(Organisation.name == name)
            )
            return await result.fetchone()
        
    async def get_organisation_by_id(self, organisation_id: int) -> Optional[OrganisationSchema]:
        result = await self.session.execute(
            select(Organisation).where(Organisation.id == organisation_id)
        )
        organisation = result.scalars().first()
        if organisation:
            return OrganisationSchema.from_orm(organisation)
        return None