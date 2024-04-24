import pytest

from app.schemas import CreateOrganisation
from pydantic import ValidationError

@pytest.fixture
def valid_data():
    return {
        "name": "ucll student",
        "username": "wompa",
        "password": "zeker"
    }


@pytest.fixture
def invalid_data():
    return {
        "name": "ucll",
        "username": "waze"
    }

def test_create_organisation_valid_data(valid_data):
    command = CreateOrganisation(**valid_data)
    assert command.name == valid_data["name"]
    assert command.username == valid_data["username"]
    assert command.password == valid_data["password"]

def test_create_organisation_invalid_data(invalid_data):
    with pytest.raises(ValidationError) as excinfo:
        CreateOrganisation(**invalid_data)
    assert "password" in str(excinfo.value)