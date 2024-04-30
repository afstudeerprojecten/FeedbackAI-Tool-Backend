import pytest
from unittest.mock import AsyncMock, patch
from app.Teacher.Service.teacherService import (
    TeacherService,
    TeacherNotFoundException,
    TeacherIdNotFoundException,
    NoTeachersFoundException,
    TeacherAlreadyExistsException,
)
from app.schemas import CreateTeacher, Teacher as TeacherSchema, UpdateTeacher as teacherSchema
import app.Teacher.Repository.teacherRepo as repo


class MockTeacherRepository(repo.InterfaceTeacherRepository):
   
    async def create_teacher(self, teacher: CreateTeacher):
        if await self.get_teacher_by_emailCheck(teacher.email):
            return None
        return TeacherSchema(id=1, name=teacher.name, lastname=teacher.lastname, email=teacher.email, organisation_id=teacher.organisation_id)
    
    async def get_teachers(self):
        return [TeacherSchema(id=2, name="John", lastname="Doe", email="john@example.com", organisation_id=2),
                TeacherSchema(id=3, name="Jane", lastname="Smith", email="jane@example.com", organisation_id=3)]
        
    async def get_teacher_by_email(self, email: str):
        if email == "test@example.com":
            return TeacherSchema(id=1, name="Test", lastname="Student", email=email, organisation_id=1)
        else:
            raise TeacherNotFoundException(email)
        
    async def get_teacher_by_emailCheck(self, email: str):
        if email == "test@example.com":
            return TeacherAlreadyExistsException
        else:
            return None

    async def get_teacher_by_firstname(self, name: str):
        if name == "Test":
            return TeacherSchema(id=1, name=name, lastname="Student", email="test@example.com", organisation_id=1)
        else:
            raise TeacherNotFoundException(name)
        
    async def get_teacher_by_id(self, id: int):
        if id == 1:
            return TeacherSchema(id=id, name="Test", lastname="Student", email="test@example.com", organisation_id=1)
        else:
            return None

    async def delete_teacher(self, teacher_id):
        if await self.get_teacher_by_id(teacher_id):
            await self.delete_teacher_by_id(teacher_id)
            return {"message": "Teacher deleted successfully"}
        else:
            raise TeacherIdNotFoundException
        
    # async def update_teacher(self, teacher_id: int, teacher_data: teacherSchema) -> repo.TeacherSchema | None:
    #     if await self.get_teacher_by_id(teacher_id):
    #         teacher = await TeacherService.update_teacher(teacher_id, teacher_data)
    #         return teacher
    #     else:
    #         raise TeacherIdNotFoundException
        

@pytest.fixture
def teacher_service():
    return TeacherService(MockTeacherRepository())


@pytest.mark.asyncio
async def test_create_teacher(teacher_service):
    teacher_data = CreateTeacher(
        name="John",
        lastname="Doe",
        email="john@example.com",
        password="password",
        organisation_id=1,
    )
    result = await teacher_service.create_teacher(teacher_data)
    assert result == {"message": "Teacher created successfully"}
        
    
@pytest.mark.asyncio
async def test_create_teacher_already_exists(teacher_service):
    teacher_data = CreateTeacher(
        name="John",
        lastname="Doe",
        email="test@example.com",
        password="password",
        organisation_id=1,
    )
    with pytest.raises(TeacherAlreadyExistsException):
        await teacher_service.create_teacher(teacher_data)


@pytest.mark.asyncio
async def test_get_teachers(teacher_service):
    teacher = await teacher_service.get_teachers()
    assert len(teacher) == 2
    assert teacher[0].name == "John"
    assert teacher[1].email == "jane@example.com"


@pytest.mark.asyncio
async def test_get_teachers_no_teachers(teacher_service):
    teacher_service.teacher_repo.get_teachers = AsyncMock(return_value=[])
    with pytest.raises(NoTeachersFoundException):
        await teacher_service.get_teachers()


@pytest.mark.asyncio
async def test_get_teacher_by_firstname_found(teacher_service):
    teacher_data = {"name": "Test", "lastname": "Student", "email": "test@example.com","password":None, "organisation_id": 1}
    teacher = await teacher_service.get_teacher_by_firstname("Test")
    assert teacher.email == teacher_data["email"]


@pytest.mark.asyncio
async def test_get_teacher_by_firstname_not_found(teacher_service):
    with pytest.raises(TeacherNotFoundException):
        await teacher_service.get_teacher_by_firstname("John")


@pytest.mark.asyncio
async def test_get_teacher_by_id_found(teacher_service):
    teacher_data = {"name": "Test", "lastname": "Student", "email": "test@example.com","password":None, "organisation_id": 1}
    teacher = await teacher_service.get_teacher_by_id(1)
    assert teacher.email == teacher_data["email"]


@pytest.mark.asyncio
async def test_get_teacher_by_id_not_found(teacher_service):
    with pytest.raises(TeacherIdNotFoundException):
        await teacher_service.get_teacher_by_id(8)


@pytest.mark.asyncio
async def test_get_teacher_by_email_found(teacher_service):
    teacher_data = {"name": "Test", "lastname": "Student", "email": "test@example.com"}
    teacher = await teacher_service.get_teacher_by_email("test@example.com")
    assert teacher.email == teacher_data["email"]


@pytest.mark.asyncio
async def test_get_teacher_by_email_not_found(teacher_service):
    with pytest.raises(TeacherNotFoundException):
        await teacher_service.get_teacher_by_email("john@example.com")
        
        
@pytest.mark.asyncio
async def test_delete_teacher_found(teacher_service):
    result = await teacher_service.delete_teacher(1)
    assert result == {"message": "Teacher deleted successfully"}

@pytest.mark.asyncio
async def test_delete_teacher_not_found(teacher_service): 
    with pytest.raises(TeacherIdNotFoundException):
        await teacher_service.delete_teacher(8)


# @pytest.mark.asyncio
# async def test_update_teacher_found(teacher_service):
#     teacher_data = {"id": 1, "name": "Jane", "lastname": "Doe", "email": "john@example.com"}
#     teacher_data2 = teacherSchema
#     expected_updated_teacher_data = {
#         "id": 1,
#         "name": "Jane",
#         "lastname": "Doe",
#         "email": "john@example.com",
#     }
    
#     updated_teacher = await teacher_service.update_teacher(1, teacher_data2)
#     assert updated_teacher.email == expected_updated_teacher_data["email"]


# @pytest.mark.asyncio
# async def test_update_teacher_not_found(teacher_service):
#     update_data = teacherSchema.UpdateTeacher(name="Jane")
#     mock_teacher_repo.get_teacher_by_id.return_value = None
#     with pytest.raises(TeacherIdNotFoundException):
#         await teacher_service.update_teacher(1, update_data)


