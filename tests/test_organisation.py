import pytest
from app.Organisation.organisationService import OrganisationService, AlreadyExistsException, NotExistsException, NotExistsIdException, NoOrganisationsFoundException
from app.schemas import Organisation, CreateOrganisation
from app.Organisation.organisationRepo import InterfaceOrganisationRepository
from fastapi import HTTPException

class MockOrganisationRepository(InterfaceOrganisationRepository):
    async def get_organisation_by_name(self, name: str):
        if name == "Test Organisation":
            return Organisation(id=1, name=name, username="test_user", password="test_password")
        else:
            return None

    async def create_organisation(self, organisation: CreateOrganisation):
        if await self.get_organisation_by_name(organisation.name):
            return None
        return Organisation(id=1, name=organisation.name, username=organisation.username, password=organisation.password)

@pytest.fixture
def organisation_service():
    return OrganisationService(MockOrganisationRepository())

@pytest.mark.asyncio
async def test_create_organisation_success(organisation_service):
    organisation = CreateOrganisation(name="Test_Organisation", username="test_user", password="test_password")
    result = await organisation_service.create_organisation(organisation)
    assert result == {"message": "Organisation created successfully"}

@pytest.mark.asyncio
async def test_create_organisation_failure(organisation_service):
    organisation = CreateOrganisation(name="Test Organisation", username="test_user", password="test_password")
    with pytest.raises(AlreadyExistsException):
        await organisation_service.create_organisation(organisation)
