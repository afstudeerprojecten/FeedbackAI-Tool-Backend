from app.models import Organisation
from app.schemas import CreateOrganisation
from app.organisationRepo import OrganisationRepository, InterfaceOrganisationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class OrganisationService():
    def __init__(self, organisation_repo: InterfaceOrganisationRepository):
        self.organisation_repo = organisation_repo
    async def create_organisation(self, organisation: CreateOrganisation):
        if await self.organisation_repo.get_organisation_by_name(organisation.name):
            raise HTTPException(status_code=400, detail="Organisation already exists")
        else:
            await self.organisation_repo.create_organisation(organisation)
            return {"message": "Organisation created successfully"}
        
    async def get_organisations(self):
        if await self.organisation_repo.get_organisations() == []:
            raise HTTPException(status_code=404, detail="No organisations found")
        else:
            organisations = await self.organisation_repo.get_organisations()
            return organisations
       
    async def get_organisation_by_name(self, name: str):
        if not await self.organisation_repo.get_organisation_by_name(name):
            raise HTTPException(status_code=404, detail="Organisation not found")
        else:
            organisation = await self.organisation_repo.get_organisation_by_name(name)
            return organisation
    
    async def get_organisation_by_id(self, organisation_id: int):
        if not await self.organisation_repo.get_organisation_by_id(organisation_id):
            raise HTTPException(status_code=404, detail="Organisation not found")
        else:
            organisation = await self.organisation_repo.get_organisation_by_id(organisation_id)
            return organisation
        
    async def delete_organisation(self, organisation_id: int):
        if not await self.organisation_repo.get_organisation_by_id(organisation_id):
            raise HTTPException(status_code=404, detail="Organisation not found")
        else:
            await self.organisation_repo.delete_organisation(organisation_id)
            return {"message": "Organisation deleted successfully"}