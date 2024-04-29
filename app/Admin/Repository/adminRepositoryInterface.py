from typing import Protocol
from app.models import Admin
from app.schemas import CreateAdmin, Admin as AdminSchema
from typing import List
from typing import Optional

class IAdminRepository(Protocol):
    async def create_admin(self, admin: CreateAdmin) -> Admin:
        ...
    
    async def get_admins(self) -> List[AdminSchema]:
        ...
    
    async def get_admin_by_id(self, admin_id: int) -> Optional[AdminSchema]:
        ...

    async def get_admin_by_username(self, username: str) -> Optional[AdminSchema]:
        ...

    async def delete_admin_by_id(self, admin_id: int) -> None:
        ...

    async def get_admin_by_usernameCheck(self, username: str) -> Optional[AdminSchema]:
        ...
        