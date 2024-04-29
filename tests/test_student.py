import pytest
from app.Student.Service.studentService import (
    StudentService,
    StudentAlreadyExistsException,
    StudentNotFoundException,
    StudentIdNotFoundException,
    NoStudentsFoundException
)
from app.schemas import CreateStudent, Student as StudentSchema
import app.Student.Repository.studentRepo as repo
from unittest.mock import AsyncMock

class MockStudentRepository(repo.InterfaceStudentRepository):
   
    async def create_student(self, student: CreateStudent):
        
        if await self.get_student_by_emailCheck(student.email):
            return None
        return StudentSchema(id=1, name=student.name, lastname=student.lastname, email=student.email, organisation_id=student.organisation_id)
    
    async def get_students(self):
        return [StudentSchema(id=2, name="John", lastname="Doe", email="john@example.com", organisation_id=2),
                StudentSchema(id=3, name="Jane", lastname="Smith", email="jane@example.com", organisation_id=3)]
        
    async def get_student_by_email(self, email: str):
        if email == "test@example.com":
            return StudentSchema(id=1, name="Test", lastname="Student", email=email, organisation_id=1)
        else:
            raise StudentNotFoundException(email)
        
    async def get_student_by_emailCheck(self, email: str):
        if email == "test@example.com":
            return StudentAlreadyExistsException
        else:
            return None

    async def get_student_by_firstname(self, name: str):
        if name == "Test":
            return StudentSchema(id=1, name=name, lastname="Student", email="test@example.com", organisation_id=1)
        else:
            return None
        
    async def get_student_by_id(self, id: int):
        if id == 1:
            return StudentSchema(id=id, name="Test", lastname="Student", email="test@example.com", organisation_id=1)
        else:
            return None
        
@pytest.fixture
def student_service():
    return StudentService(MockStudentRepository())

@pytest.mark.asyncio
async def test_create_student_success(student_service):
    student = CreateStudent(name="Te123st2", lastname="Stud123ent2", email="rand132om@example.com", password="password", organisation_id=5)
    result = await student_service.create_student(student)
    assert result == {"message": "Student created successfully"}

@pytest.mark.asyncio
async def test_create_student_failure(student_service):
    student = CreateStudent(name="Test", lastname="Student", email="test@example.com", password="password", organisation_id=1)
    with pytest.raises(StudentAlreadyExistsException):
        await student_service.create_student(student)
        
@pytest.mark.asyncio
async def test_get_students_success(student_service):
    students = await student_service.get_students()
    assert len(students) == 2
    assert students[0].name == "John"
    assert students[1].email == "jane@example.com"

@pytest.mark.asyncio
async def test_get_students_no_students_found(student_service):
    student_service.student_repo.get_students = AsyncMock(return_value=[])
    with pytest.raises(NoStudentsFoundException):
        await student_service.get_students()
    
    
@pytest.mark.asyncio
async def test_get_student_by_email_success(student_service):
    student = await student_service.get_student_by_email("test@example.com")
    assert student.id == 1
    assert student.name == "Test"
    assert student.lastname == "Student"

@pytest.mark.asyncio
async def test_get_student_by_email_not_found(student_service):
    with pytest.raises(StudentNotFoundException):
        await student_service.get_student_by_email("nonexistent@example.com")
        

@pytest.mark.asyncio
async def test_get_student_by_firstname_success(student_service): 
    student = await student_service.get_student_by_firstname("Test")
    assert student.id == 1
    assert student.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_student_by_firstname_not_found(student_service):
    with pytest.raises(StudentNotFoundException):
        await student_service.get_student_by_firstname("Nonexistent")
        
@pytest.mark.asyncio
async def test_get_student_by_id_success(student_service): 
    student = await student_service.get_student_by_id(1)
    assert student.id == 1
    assert student.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_student_by_id_not_found(student_service):
    with pytest.raises(StudentIdNotFoundException):
        await student_service.get_student_by_id(5)

