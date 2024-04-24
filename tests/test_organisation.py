import pytest
from app.organisationRepo import OrganisationService, InterfaceOrganisationRepository
from app.schemas import CreateOrganisation
from app.models import Organisation
from unittest.mock import AsyncMock

@pytest.fixture
def mock_organisation_repo():
    return AsyncMock(spec=InterfaceOrganisationRepository)

@pytest.fixture
def organisation_service(mock_organisation_repo):
    return OrganisationService(mock_organisation_repo)

@pytest.mark.asyncio
async def test_organisation_service_create_organisation(organisation_service, mock_organisation_repo):
    # GIVEN
    create_organisation_data = CreateOrganisation(
        name="TestOrg", username="testuser", password="testpassword"
    )
    expected_organisation = Organisation(id=1, name="TestOrg", username="testuser", password="hashed_password")

    # Mocking the behaviour of OrganisationRepository.create_organisation method
    mock_organisation_repo.create_organisation.return_value = expected_organisation

    # WHEN
    organisation = await organisation_service.create_organisation(create_organisation_data)

    # THEN
    mock_organisation_repo.create_organisation.assert_called_once_with(create_organisation_data)
    assert organisation == expected_organisation
