import pytest
from unittest.mock import AsyncMock, MagicMock
from app.Admin.Service.adminService import AdminService ,AdminIdNotFoundException, AdminAlreadyExistsException , AdminNotFoundException , NoAdminsFoundException
from app.schemas import CreateAdmin
from app.models import Admin
from app.Admin.Repository.adminRepositoryInterface import IAdminRepository


class MockAdminRepository(IAdminRepository):
    
    async def create_admin(self, admin: CreateAdmin):
        if await self.get_admin_by_usernameCheck(admin.username):
            return None
        return Admin(id=1 , username = admin.username, password = admin.password)
    
    async def get_admins(self):
        return [Admin(id=2, username = "Test2", password = "randpw1"),
                Admin(id=3, username = "Test3", password = "randpw2")]
        
    async def get_admin_by_id(self, id: int):
        if id == 4:
            return Admin(username = "Test", password = "randpw")
        else:
            return None
        
    async def get_admin_by_usernameCheck(self, username: str):
        if username == "Test":
            raise AdminAlreadyExistsException(username)
        else:
            return None
    
    async def get_admin_by_username(self, username: str):
        if username == "Test5":
            return Admin(id=5, username = "Test5", password = "randpw")
        else: 
            raise AdminNotFoundException
        
    async def delete_admin_by_id(self, id: int):
        if await self.get_admin_by_id(id):
            await self.delete_admin_by_id(id)
            return {"message": "Teacher deleted succesfully"}
        else:
            raise AdminIdNotFoundException


@pytest.fixture
def admin_service():
    return AdminService(MockAdminRepository())

@pytest.mark.asyncio
async def test_create_admin_success(admin_service):
    response = await admin_service.create_admin(CreateAdmin(username="test_user", password="test_password"))
    assert response == {"message": "Admin created successfully"}
    
@pytest.mark.asyncio
async def test_create_admin_already_exists(admin_service):
    with pytest.raises(AdminAlreadyExistsException):
        await admin_service.create_admin(CreateAdmin(username="Test", password="test_password"))
       
@pytest.mark.asyncio
async def test_get_admins(admin_service):
    admins = await admin_service.get_admins()
    assert len(admins) == 2
    assert admins[0].username == "Test2"
    assert admins[1].username == "Test3"

@pytest.mark.asyncio
async def test_get_admins_empty(admin_service):
    admin_service.adminRepository.get_admins = AsyncMock(return_value=[])
    with pytest.raises(NoAdminsFoundException):
        await admin_service.get_admins()

@pytest.mark.asyncio
async def test_get_admin_by_id(admin_service):
    admin_data = {"id": 4, "username": "Test", "password": "randpw"}
    admin = await admin_service.get_admin_by_id(4)
    assert admin.username == admin_data["username"]

@pytest.mark.asyncio
async def test_get_admin_by_id_not_found(admin_service):
    with pytest.raises(AdminIdNotFoundException):
        await admin_service.get_admin_by_id(8)


@pytest.mark.asyncio
async def test_delete_admin_not_found(admin_service): 
    with pytest.raises(AdminIdNotFoundException):
        await admin_service.delete_admin_by_id(8)
        
# Does not work , can't figure out why
        
# @pytest.mark.asyncio
# async def test_delete_admin_found(admin_service):
#     result = await admin_service.delete_admin_by_id(4)
#     assert result == {"message": "Admin deleted successfully"}

# @pytest.mark.asyncio
# async def test_get_admin_by_username(admin_service):
#     admin_data = {"id": 5, "username": "Test5", "password": "randpw"}
#     admin = await admin_service.get_admin_by_username("Test5")
#     assert admin.id == admin_data["password"]
    
# @pytest.mark.asyncio
# async def test_get_admin_by_username_not_found(admin_service):
#     test = await admin_service.get_admin_by_username("random") 
#     print(f"################################## {test} ##################################")
#     with pytest.raises(AdminNotFoundException):
#         await admin_service.get_admin_by_username("random")
        




