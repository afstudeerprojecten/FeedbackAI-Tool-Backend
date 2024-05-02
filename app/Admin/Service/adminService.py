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


class AdminAlreadyExistsException(Exception):
    def __init__(self, username: str):
        self.username = username

class AdminNotFoundException(Exception):
    def __init__(self, username: str):
        self.username = username

class AdminIdNotFoundException(Exception):
    def __init__(self, admin_id: int):
        self.admin_id = admin_id

class NoAdminsFoundException(Exception):
    def __init__(self):
        pass

@dataclass
class AdminService:

    adminRepository: IAdminRepository

    @classmethod
    def from_async_repo(cls, session: AsyncSession) -> Self:
        adminRepository = AdminRepositoryAsync(session=session)
        return AdminService(adminRepository=adminRepository)
    
    async def create_admin(self, admin: CreateAdmin) -> Admin:
        if await self.adminRepository.get_admin_by_usernameCheck(admin.username):
            raise AdminAlreadyExistsException(admin.username)
        else:
            await self.adminRepository.create_admin(admin=admin)
            return {"message": "Admin created successfully"}
    
    async def get_admins(self) -> List[AdminSchema]:
        if await self.adminRepository.get_admins() == []:
            raise NoAdminsFoundException()
        else:
            return await self.adminRepository.get_admins()
        
    async def get_admin_by_id(self, admin_id: int) -> Optional[AdminSchema]:
        if not await self.adminRepository.get_admin_by_id(admin_id):
            raise AdminIdNotFoundException(admin_id)
        else:
            return await self.adminRepository.get_admin_by_id(admin_id)
    
    async def get_admin_by_usernameCheck(self, username: str) -> Optional[AdminSchema]:
        admin = await self.adminRepository.get_admin_by_username(username=username)
        if admin:
            return admin
        else:
            None
        
    async def get_admin_by_username(self, username: str) -> Optional[AdminSchema]:
        if await self.adminRepository.get_admin_by_usernameCheck(username):
            return await self.adminRepository.get_admin_by_usernameCheck(username)
        else:
            return AdminNotFoundException(username)
    
    async def delete_admin_by_id(self, admin_id: int) -> None:
        if not await self.adminRepository.get_admin_by_id(admin_id):
            raise AdminIdNotFoundException(admin_id)
        else:
            await self.adminRepository.delete_admin_by_id(admin_id)
            return {"message": "Admin deleted successfully"}