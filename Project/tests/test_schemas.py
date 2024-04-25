import pytest

from app.schemas import CreateOrganisation
from app.schemas import Organisation
from pydantic import ValidationError


# used to create the data for the test
@pytest.fixture
def valid_data_create():
    return {
        "name": "ucll student",
        "username": "wompa",
        "password": "zeker"
    }


@pytest.fixture
def invalid_data_create():
    return {
        "name": "ucll",
        "username": "waze"
    }

# functions for the create organisation,
# checks both the valid and invalid input
def test_create_organisation_valid_data(valid_data_create):
    command = CreateOrganisation(**valid_data_create)
    assert command.name == valid_data_create["name"]
    assert command.username == valid_data_create["username"]
    assert command.password == valid_data_create["password"]

def test_create_organisation_invalid_data(invalid_data_create):
    with pytest.raises(ValidationError) as excinfo:
        CreateOrganisation(**invalid_data_create)
    assert "password" in str(excinfo.value)

#####################################################################


@pytest.fixture
def valid_data_organisation():
    return{
        "id": 1,
        "name": "justin",
        "username": "justinh"
    }

@pytest.fixture
def invalid_data_organisation():
    return{
        "name": "justin",
        "username": "justinh"
    }

def test_organisation_valid_data(valid_data_organisation):
    organisation = Organisation(**valid_data_organisation)
    assert organisation.id == valid_data_organisation["id"]
    assert organisation.name == valid_data_organisation["name"]
    assert organisation.username == valid_data_organisation["username"]

def test_organisation_invalid_data(invalid_data_organisation):
    with pytest.raises(ValidationError) as excinfo:
        CreateOrganisation(**invalid_data_organisation)
    assert "id" in str(excinfo.value)