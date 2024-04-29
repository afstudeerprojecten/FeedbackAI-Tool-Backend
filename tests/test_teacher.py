import pytest
from unittest.mock import AsyncMock, patch
from app.Teacher.Service.teacherService import (
    TeacherService,
    TeacherNotFoundException,
    TeacherIdNotFoundException,
    NoTeachersFoundException,
    TeacherAlreadyExistsException,
)
from app.schemas import CreateTeacher, UpdateTeacher


@pytest.fixture
def mock_teacher_repo():
    return AsyncMock()


@pytest.fixture
def teacher_service(mock_teacher_repo):
    return TeacherService(mock_teacher_repo)


@pytest.mark.asyncio
async def test_create_teacher(teacher_service, mock_teacher_repo):
    teacher_data = CreateTeacher(
        name="John",
        lastname="Doe",
        email="john@example.com",
        password="password",
        organisation_id=1,
    )
    mock_teacher_repo.get_teacher_by_emailCheck.return_value = None
    await teacher_service.create_teacher(teacher_data)
    mock_teacher_repo.create_teacher.assert_called_once_with(teacher_data) 
    
     
    
@pytest.mark.asyncio
async def test_create_teacher_already_exists(teacher_service, mock_teacher_repo):
    teacher_data = CreateTeacher(
        name="John",
        lastname="Doe",
        email="john@example.com",
        password="password",
        organisation_id=1,
    )
    mock_teacher_repo.get_teacher_by_emailCheck.return_value = True
    with pytest.raises(TeacherAlreadyExistsException):
        await teacher_service.create_teacher(teacher_data)


@pytest.mark.asyncio
async def test_get_teachers(teacher_service, mock_teacher_repo):
    mock_teacher_repo.get_teachers.return_value = [
        {"name": "John", "lastname": "Doe", "email": "john@example.com"}
    ]
    teachers = await teacher_service.get_teachers()
    assert len(teachers) == 1
    assert teachers[0]["name"] == "John"


@pytest.mark.asyncio
async def test_get_teachers_no_teachers(teacher_service, mock_teacher_repo):
    mock_teacher_repo.get_teachers.return_value = []
    with pytest.raises(NoTeachersFoundException):
        await teacher_service.get_teachers()


@pytest.mark.asyncio
async def test_get_teacher_by_firstname_found(teacher_service, mock_teacher_repo):
    teacher_data = {"name": "John", "lastname": "Doe", "email": "john@example.com"}
    mock_teacher_repo.get_teacher_by_firstname.return_value = teacher_data
    teacher = await teacher_service.get_teacher_by_firstname("John")
    assert teacher == teacher_data


@pytest.mark.asyncio
async def test_get_teacher_by_firstname_not_found(
    teacher_service, mock_teacher_repo
):
    mock_teacher_repo.get_teacher_by_firstname.return_value = None
    with pytest.raises(TeacherNotFoundException):
        await teacher_service.get_teacher_by_firstname("John")


@pytest.mark.asyncio
async def test_get_teacher_by_id_found(teacher_service, mock_teacher_repo):
    teacher_data = {"name": "John", "lastname": "Doe", "email": "john@example.com"}
    mock_teacher_repo.get_teacher_by_id.return_value = teacher_data
    teacher = await teacher_service.get_teacher_by_id(1)
    assert teacher == teacher_data


@pytest.mark.asyncio
async def test_get_teacher_by_id_not_found(teacher_service, mock_teacher_repo):
    mock_teacher_repo.get_teacher_by_id.return_value = None
    with pytest.raises(TeacherIdNotFoundException):
        await teacher_service.get_teacher_by_id(1)


@pytest.mark.asyncio
async def test_delete_teacher_found(teacher_service, mock_teacher_repo):
    mock_teacher_repo.get_teacher_by_id.return_value = {"id": 1}
    await teacher_service.delete_teacher(1)
    mock_teacher_repo.delete_teacher_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_delete_teacher_not_found(teacher_service, mock_teacher_repo):
    mock_teacher_repo.get_teacher_by_id.return_value = None
    with pytest.raises(TeacherIdNotFoundException):
        await teacher_service.delete_teacher(1)


@pytest.mark.asyncio
async def test_update_teacher_found(teacher_service, mock_teacher_repo):
    teacher_data = {"id": 1, "name": "John", "lastname": "Doe", "email": "john@example.com"}
    update_data = UpdateTeacher(name="Jane")
    expected_updated_teacher_data = {
        "id": 1,
        "name": "Jane",
        "lastname": "Doe",
        "email": "john@example.com",
    }
    mock_teacher_repo.get_teacher_by_id.return_value = teacher_data
    mock_teacher_repo.update_teacher.return_value = expected_updated_teacher_data

    updated_teacher = await teacher_service.update_teacher(1, update_data)
    assert updated_teacher == expected_updated_teacher_data


@pytest.mark.asyncio
async def test_update_teacher_not_found(teacher_service, mock_teacher_repo):
    update_data = UpdateTeacher(name="Jane")
    mock_teacher_repo.get_teacher_by_id.return_value = None
    with pytest.raises(TeacherIdNotFoundException):
        await teacher_service.update_teacher(1, update_data)


@pytest.mark.asyncio
async def test_get_teacher_by_email_found(teacher_service, mock_teacher_repo):
    teacher_data = {"name": "John", "lastname": "Doe", "email": "john@example.com"}
    mock_teacher_repo.get_teacher_by_email.return_value = teacher_data
    teacher = await teacher_service.get_teacher_by_email("john@example.com")
    assert teacher["email"] == teacher_data["email"]


@pytest.mark.asyncio
async def test_get_teacher_by_email_not_found(teacher_service, mock_teacher_repo):
    mock_teacher_repo.get_teacher_by_email.return_value = None
    with pytest.raises(TeacherNotFoundException):
        await teacher_service.get_teacher_by_email("john@example.com")
