from dataclasses import dataclass
from app.models import Student
from app.schemas import CreateStudent, Student as StudentSchema
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Protocol

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class InterfaceStudentRepository(Protocol):
    async def create_student(self, student: CreateStudent) -> Student:
        ...

    async def get_students(self) -> List[StudentSchema]:
        ...

    async def get_student_by_id(self, student_id: int) -> Optional[StudentSchema]:
        ...

    async def get_student_by_firstname(self, name: str) -> Optional[StudentSchema]:
        ...

    async def delete_student_by_id(self, student_id: int) -> None:
        ...

    async def get_student_by_email(self, email: str) -> Optional[StudentSchema]:
        ...
    
    async def get_student_by_emailCheck(self, email: str) -> Optional[StudentSchema]:
        ...

    async def get_organisation_id_by_student_id(self, student_id: int) -> Optional[int]:
        ...


@dataclass
class StudentRepository:
    session: AsyncSession
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_student(self, student: CreateStudent) -> Student:
        hashed_password = pwd_context.hash(student.password)
        new_student = Student(name=student.name, lastname=student.lastname, email=student.email, password=hashed_password, organisation_id=student.organisation_id)
        self.session.add(new_student)
        await self.session.commit()
        return new_student
    
    async def get_students(self) -> List[StudentSchema]:
        result = await self.session.execute(select(Student))
        students = [StudentSchema.from_orm(student) for student in result.scalars()]
        return students
    
    async def get_student_by_id(self, student_id: int) -> Optional[StudentSchema]:
        result = await self.session.execute(
            select(Student).where(Student.id == student_id)
        )
        student = result.scalars().first()
        if student:
            return StudentSchema.from_orm(student)
        return None
    
    async def get_student_by_firstname(self, name: str) -> Optional[StudentSchema]:
            result = await self.session.execute(
                select(Student).where(Student.name == name)
            )
            student = result.scalars().first()
            if student:
                return StudentSchema.from_orm(student)
            return None
    
    async def delete_student_by_id(self, student_id: int) -> None:
        result = await self.session.execute(
            select(Student).where(Student.id == student_id)
            )
        student = result.scalars().first()        
        if student:
            await self.session.delete(student)
            await self.session.commit()

    async def get_student_by_email(self, email: str) -> Optional[StudentSchema]:
        result = await self.session.execute(
            select(Student).where(Student.email == email)
        )
        student = result.scalars().first()
        if student:
            return StudentSchema.from_orm(student)
        return None
    
    async def get_student_by_emailCheck(self, email: str) -> Optional[StudentSchema]:
        result = await self.session.execute(
            select(Student).where(Student.email == email)
        )
        student = result.scalars().first()
        if student:
            return StudentSchema.from_orm(student)
        return None

    # async def update_Student(self, Student_id: int, Student_data: UpdateStudent) -> Optional[StudentSchema]:
    #     result = await self.session.execute(
    #         select(Student).where(Student.id == Student_id)
    #     )
    #     Student = result.scalars().first()
    #     if not Student:
    #         return None

    #     # Update only the provided fields from Student_data
    #     for key, value in Student_data.dict(exclude_unset=True).items():
    #         setattr(Student, key, value)

    #     await self.session.commit()
    #     # Refresh the Student object to reflect the changes in the database
    #     await self.session.refresh(Student)
    #     return StudentSchema.from_orm(Student)
