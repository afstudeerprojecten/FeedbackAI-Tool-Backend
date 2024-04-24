from app.models import Organisation
from app.schemas import CreateOrganisation
from app.organisationRepo import OrganisationRepository, InterfaceOrganisationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class OrganisationService():
    def __init__(self, organisation_repo: InterfaceOrganisationRepository):
        self.organisation_repo = organisation_repo
    async def create_organisation(organisation: CreateOrganisation) -> Organisation:
        return await InterfaceOrganisationRepository.create_organisation(organisation)
       