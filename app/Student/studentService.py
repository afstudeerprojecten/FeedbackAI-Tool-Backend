from app.models import Student
from app.schemas import CreateStudent, Student as StudentSchema
from app.Student.studentRepo import Student, InterfaceStudentRepository
from sqlalchemy.ext.asyncio import AsyncSession


class StudentAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name

class StudentNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

class StudentIdNotFoundException(Exception):
    def __init__(self, student_id: int):
        self.student_id = student_id

class NoStudentsFoundException(Exception):
    def __init__(self):
        pass

class StudentService():
    def __init__(self, student_repo: InterfaceStudentRepository):
        self.student_repo = student_repo
    async def create_student(self, student: CreateStudent):
        if await self.student_repo.get_student_by_email(student.email):
            raise StudentAlreadyExistsException(student.email)
        else:
            await self.student_repo.create_student(student)
            return {"message": "Student created successfully"}

        
    async def get_students(self):
        if await self.student_repo.get_students() == []:
            raise NoStudentsFoundException()
        else:
            students = await self.student_repo.get_students()
            return students
       
    async def get_student_by_firstname(self, name: str):
        student = await self.student_repo.get_student_by_firstname(name)
        if student is None:
            raise StudentNotFoundException(name)
        return student

    
    async def get_student_by_id(self, student_id: int):
        if not await self.student_repo.get_student_by_id(student_id):
            raise StudentIdNotFoundException(student_id)
        else:
            student = await self.student_repo.get_student_by_id(student_id)
            return student
        
    async def delete_student(self, student_id: int):
        if not await self.student_repo.get_student_by_id(student_id):
            raise StudentIdNotFoundException(student_id)
        else:
            await self.student_repo.delete_student_by_id(student_id)
            return {"message": "Student deleted successfully"}
        
    async def get_student_by_email(self, email: str):
        student = await self.student_repo.get_student_by_email(email)
        if student:
            return student
        else:
            return None
    