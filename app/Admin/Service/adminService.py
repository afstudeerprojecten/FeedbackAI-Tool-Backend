from re import A
from typing import Self
from app.Admin.Repository.adminRepoAsync import AdminRepositoryAsync
from app.Admin.Repository.adminRepositoryInterface import IAdminRepository
from sqlalchemy.ext.asyncio import AsyncSession
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

@dataclass
class AdminService:

    adminRepository: IAdminRepository

    @classmethod
    def from_async_repo(cls, session: AsyncSession) -> Self:
        adminRepository = AdminRepositoryAsync(session=session)
        return AdminService(adminRepository=adminRepository)
    
    async def create_admin(self, admin: CreateAdmin) -> Admin:
        return await self.adminRepository.create_admin(admin=admin)
    
    async def get_admins(self) -> List[AdminSchema]:
        return await self.adminRepository.get_admins()
        
    async def get_admin_by_id(self, admin_id: int) -> Optional[AdminSchema]:
        return await self.adminRepository.get_admin_by_id(admin_id=admin_id)
    
    async def get_admin_by_username(self, username: str) -> Optional[AdminSchema]:
        return await self.adminRepository.get_admin_by_username(username=username)
    
    async def delete_admin_by_id(self, admin_id: int) -> None:
        return await self.adminRepository.delete_admin_by_id(admin_id=admin_id)