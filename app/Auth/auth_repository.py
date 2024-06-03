# repositories/auth_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Teacher, Student

class AuthRepository:
    async def get_user_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(Teacher).filter(Teacher.email == email))
        user = result.scalars().first()
        if user:
            return user, 'teacher'
        result = await db.execute(select(Student).filter(Student.email == email))
        user = result.scalars().first()
        if user:
            return user, 'student'
        return None, None
