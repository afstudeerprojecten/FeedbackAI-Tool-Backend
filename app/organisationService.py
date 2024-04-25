from app.models import Organisation
from app.schemas import CreateOrganisation
from app.organisationRepo import OrganisationRepository, InterfaceOrganisationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class AlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name

class NotExistsException(Exception):
    def __init__(self, name: str):
        self.name = name
class NotExistsIdException(Exception):
    def __init__(self, organisation_id: int):
        self.organisation_id = organisation_id
class NoOrganisationsFoundException(Exception):
    def __init__(self):
        pass

class OrganisationService():
    def __init__(self, organisation_repo: InterfaceOrganisationRepository):
        self.organisation_repo = organisation_repo
    async def create_organisation(self, organisation: CreateOrganisation):
        if await self.organisation_repo.get_organisation_by_name(organisation.name):
            raise AlreadyExistsException(organisation.name)
        else:
            await self.organisation_repo.create_organisation(organisation)
            return {"message": "Organisation created successfully"}
        
    async def get_organisations(self):
        if await self.organisation_repo.get_organisations() == []:
            raise NoOrganisationsFoundException()
        else:
            organisations = await self.organisation_repo.get_organisations()
            return organisations
       
    async def get_organisation_by_name(self, name: str):
        organisation = await self.organisation_repo.get_organisation_by_name(name)
        if organisation:
            return organisation
        else:
            return None
    
    async def get_organisation_by_id(self, organisation_id: int):
        if not await self.organisation_repo.get_organisation_by_id(organisation_id):
            raise NotExistsIdException(organisation_id)
        else:
            organisation = await self.organisation_repo.get_organisation_by_id(organisation_id)
            return organisation
        
    async def delete_organisation(self, organisation_id: int):
        if not await self.organisation_repo.get_organisation_by_id(organisation_id):
            raise NotExistsIdException(organisation_id)
        else:
            await self.organisation_repo.delete_organisation(organisation_id)
            return {"message": "Organisation deleted successfully"}