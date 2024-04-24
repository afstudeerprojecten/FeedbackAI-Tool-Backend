from dataclasses import dataclass
from app.models import Organisation
from app.schemas import CreateOrganisation, Organisation as OrganisationSchema
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Protocol


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from dataclasses import dataclass


class InterfaceOrganisationRepository(Protocol):
    async def create_organisation(self, organisation: CreateOrganisation) -> Organisation:
        ...

    async def get_organisations(self) -> List[OrganisationSchema]:
        ...

    async def get_organisation_by_name(self, name: str) -> Optional[OrganisationSchema]:
        ...

    async def get_organisation_by_id(self, organisation_id: int) -> Optional[OrganisationSchema]:
        ...

    async def delete_organisation(self, organisation_id: int) -> None:
        ...

@dataclass
class OrganisationService:
        organisation_repo: InterfaceOrganisationRepository

        async def create_organisation(self, organisation: CreateOrganisation) -> Organisation:
            return await self.organisation_repo.create_organisation(organisation)
        
        async def get_organisations(self) -> List[OrganisationSchema]:
            return await self.organisation_repo.get_organisations()
        
        async def get_organisation_by_name(self, name: str) -> Optional[OrganisationSchema]:
            return await self.organisation_repo.get_organisation_by_name(name)
        
        async def get_organisation_by_id(self, organisation_id: int) -> Optional[OrganisationSchema]:
            return await self.organisation_repo.get_organisation_by_id(organisation_id)
        
        async def delete_organisation(self, organisation_id: int) -> None:
            return await self.organisation_repo.delete_organisation(organisation_id)
        
    
def generate_service(session: AsyncSession) -> OrganisationService:
        repo = OrganisationRepository(session)
        return OrganisationService(repo)

@dataclass
class OrganisationRepository:
    """
    Repository class for managing organisations in the database.
    """

    session: AsyncSession
    

    async def create_organisation(self, organisation: CreateOrganisation) -> Organisation:
        """
        Creates a new organisation in the database.

        Args:
            organisation (CreateOrganisation): The details of the organisation to be created.

        Returns:
            Organisation: The created organisation.
        """
        hashed_password = pwd_context.hash(organisation.password)
        new_organisation = Organisation(name=organisation.name, username=organisation.username, password=hashed_password)
        self.session.add(new_organisation)
        await self.session.commit()
        return new_organisation
    
    async def get_organisations(self) -> List[OrganisationSchema]:
        """
        Retrieves all organisations from the database.

        Returns:
            List[OrganisationSchema]: A list of organisation schemas.
        """
        result = await self.session.execute(select(Organisation))
        organisations = [OrganisationSchema.from_orm(org) for org in result.scalars()]
        return organisations

    async def get_organisation_by_name(self, name: str) -> Optional[OrganisationSchema]:
        """
        Retrieves an organisation from the database by its name.

        Args:
            name (str): The name of the organisation.

        Returns:
            Optional[OrganisationSchema]: The organisation schema if found, None otherwise.
        """
        result = await self.session.execute(
            select(Organisation).where(Organisation.name == name)
        )
        organisation = result.scalars().first()
        if organisation:
            return OrganisationSchema.from_orm(organisation)
        return None
        
    async def get_organisation_by_id(self, organisation_id: int) -> Optional[OrganisationSchema]:
        """
        Retrieves an organisation from the database by its ID.

        Args:
            organisation_id (int): The ID of the organisation.

        Returns:
            Optional[OrganisationSchema]: The organisation schema if found, None otherwise.
        """
        result = await self.session.execute(
            select(Organisation).where(Organisation.id == organisation_id)
        )
        organisation = result.scalars().first()
        if organisation:
            return OrganisationSchema.from_orm(organisation)
        return None

    async def delete_organisation(self, organisation_id: int) -> None:
        """
        Deletes an organisation from the database by its ID.

        Args:
            organisation_id (int): The ID of the organisation to be deleted.
        """
        result = await self.session.execute(
            select(Organisation).where(Organisation.id == organisation_id)
        )
        organisation = result.scalars().first()
        if organisation:
            await self.session.delete(organisation)
            await self.session.commit()
        return None
    


