from dataclasses import dataclass
from app.Admin.Repository.adminRepositoryInterface import IAdminRepository
from app.models import Admin
from app.schemas import CreateAdmin, Admin as AdminSchema
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class AdminRepositoryAsync(IAdminRepository):
    session: AsyncSession
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_admin(self, admin: CreateAdmin) -> Admin:
        hashed_password = pwd_context.hash(admin.password)
        new_admin = Admin(username=admin.username, password=hashed_password)
        self.session.add(new_admin)
        await self.session.commit()
        return new_admin
    
    async def get_admins(self) -> List[AdminSchema]:
        result = await self.session.execute(select(Admin))
        admins = [AdminSchema.from_orm(org) for org in result.scalars()]
        return admins
    
    async def get_admin_by_id(self, admin_id: int) -> Optional[AdminSchema]:
        result = await self.session.execute(
            select(Admin).where(Admin.id == admin_id)
        )
        admin = result.scalars().first()
        if admin:
            return AdminSchema.from_orm(admin)
        return None

    async def get_admin_by_username(self, username: str) -> Optional[AdminSchema]:
        result = await self.session.execute(
            select(Admin).where(Admin.username == username)
        )
        admin = result.scalars().first()
        if admin:
            return AdminSchema.from_orm(admin)
        return None

    async def delete_admin_by_id(self, admin_id: int) -> None:
        result = await self.session.execute(
            select(Admin).where(Admin.id == admin_id)
            )
        admin = result.scalars().first()        
        if admin:
            await self.session.delete(admin)
            await self.session.commit()
    
    