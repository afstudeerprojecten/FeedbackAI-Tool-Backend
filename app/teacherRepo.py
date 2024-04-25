from dataclasses import dataclass
from app.models import Teacher
from app.schemas import CreateTeacher, Teacher as TeacherSchema, UpdateTeacher
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Protocol

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class InterfaceTeacherRepository(Protocol):
    async def create_teacher(self, teacher: CreateTeacher) -> Teacher:
        ...

    async def get_teachers(self) -> List[TeacherSchema]:
        ...

    async def get_teacher_by_id(self, teacher_id: int) -> Optional[TeacherSchema]:
        ...

    async def get_teacher_by_firstname(self, name: str) -> Optional[TeacherSchema]:
        ...

    async def delete_teacher_by_id(self, teacher_id: int) -> None:
        ...

    async def update_teacher(self, teacher_id: int, teacher_data: UpdateTeacher) -> Optional[TeacherSchema]:
        ...

    async def get_teacher_by_email(self, email: str) -> Optional[TeacherSchema]:
        ...

@dataclass
class TeacherRepository:
    session: AsyncSession
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_teacher(self, teacher: CreateTeacher) -> Teacher:
        hashed_password = pwd_context.hash(teacher.password)
        new_teacher = Teacher(name=teacher.name, lastname=teacher.lastname, email=teacher.email, password=hashed_password, organisation_id=teacher.organisation_id)
        self.session.add(new_teacher)
        await self.session.commit()
        return new_teacher
    
    async def get_teachers(self) -> List[TeacherSchema]:
        result = await self.session.execute(select(Teacher))
        teachers = [TeacherSchema.from_orm(teacher) for teacher in result.scalars()]
        return teachers
    
    async def get_teacher_by_id(self, teacher_id: int) -> Optional[TeacherSchema]:
        result = await self.session.execute(
            select(Teacher).where(Teacher.id == teacher_id)
        )
        teacher = result.scalars().first()
        if teacher:
            return TeacherSchema.from_orm(teacher)
        return None
    
    async def get_teacher_by_firstname(self, name: str) -> Optional[TeacherSchema]:
            result = await self.session.execute(
                select(Teacher).where(Teacher.name == name)
            )
            teacher = result.scalars().first()
            if teacher:
                return TeacherSchema.from_orm(teacher)
            return None
    
    async def delete_teacher_by_id(self, teacher_id: int) -> None:
        result = await self.session.execute(
            select(Teacher).where(Teacher.id == teacher_id)
            )
        teacher = result.scalars().first()        
        if teacher:
            await self.session.delete(teacher)
            await self.session.commit()

    async def update_teacher(self, teacher_id: int, teacher_data: UpdateTeacher) -> Optional[TeacherSchema]:
        result = await self.session.execute(
            select(Teacher).where(Teacher.id == teacher_id)
        )
        teacher = result.scalars().first()
        if not teacher:
            return None

        # Update only the provided fields from teacher_data
        for key, value in teacher_data.dict(exclude_unset=True).items():
            setattr(teacher, key, value)

        await self.session.commit()
        # Refresh the teacher object to reflect the changes in the database
        await self.session.refresh(teacher)
        return TeacherSchema.from_orm(teacher)
    
    async def get_teacher_by_email(self, email: str) -> Optional[TeacherSchema]:
        result = await self.session.execute(
            select(Teacher).where(Teacher.email == email)
        )
        teacher = result.scalars().first()
        if teacher:
            return TeacherSchema.from_orm(teacher)
        return None
