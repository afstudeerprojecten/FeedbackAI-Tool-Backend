from app.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from app.models import Student
from app.schemas import CreateStudent, Student as StudentSchema
from app.Student.Repository.studentRepo import Student, InterfaceStudentRepository
from sqlalchemy.ext.asyncio import AsyncSession

class StudentService():
    def __init__(self, student_repo: InterfaceStudentRepository):
        self.student_repo = student_repo

    async def create_student(self, student: CreateStudent):
        if await self.student_repo.get_student_by_emailCheck(student.email):
            raise EntityAlreadyExistsException(f"student with email {student.email} not found")
        else:
            await self.student_repo.create_student(student)
            return {"message": "Student created successfully"}

    async def get_students(self):
        if await self.student_repo.get_students() == []:
            raise EntityNotFoundException("No students found")
        else:
            students = await self.student_repo.get_students()
            return students

    async def get_student_by_firstname(self, name: str):
        student = await self.student_repo.get_student_by_firstname(name)
        if student is None:
            raise EntityNotFoundException(name)
        return student

    async def get_student_by_id(self, student_id: int):
        if not await self.student_repo.get_student_by_id(student_id):
            raise EntityNotFoundException(f"student with id {student_id} not found")
        else:
            student = await self.student_repo.get_student_by_id(student_id)
            return student

    async def delete_student(self, student_id: int):
        if not await self.student_repo.get_student_by_id(student_id):
            raise EntityNotFoundException(f"student with id {student_id} not found")
        else:
            await self.student_repo.delete_student_by_id(student_id)
            return {"message": "Student deleted successfully"}

    async def get_student_by_email(self, email: str):
        student = await self.student_repo.get_student_by_email(email)
        if student:
            return student
        else:
            return None

    async def get_student_by_emailCheck(self, email: str):
        if await self.student_repo.get_student_by_emailCheck(email):
            return await self.student_repo.get_student_by_emailCheck(email)
        else:
            raise EntityNotFoundException(f"student with email {email} not found")

    async def get_student_name_by_id(self, student_id: int):
        student = await self.student_repo.get_student_by_id(student_id)
        if student:
            return student.name + " " + student.lastname
        else:
            raise EntityNotFoundException(f"student with id {student_id} not found")