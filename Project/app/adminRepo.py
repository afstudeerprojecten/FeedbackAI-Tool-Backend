from dataclasses import dataclass    
import app.models as models
from sqlalchemy import Engine
from app.schemas import CreateAdmin, Admin
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Protocol, List


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminRepositoryInterface(Protocol):
    def create_admin(self, admin: CreateAdmin) -> models.Admin:
        ...

@dataclass
class AdminRepository:
    engine: Engine
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
    def create_admin(self, admin: CreateAdmin) -> models.Admin:
        hashed_password = pwd_context.hash(admin.password)
        with self.engine.connect() as conn:
            conn.execute(
                models.Admin.__table__.insert().values(
                    username=admin.username,
                    password=hashed_password
            )
        )
        conn.commit()
        return models.Admin(username=admin.username, password=hashed_password)
    def get_admins(self) -> List[Admin]:
        with self.engine.connect() as conn:
            result = conn.execute(models.Admin.__table__.select())
            admins = []
            for row in result.fetchall():
                admin_data = dict(row._asdict())
                admin = Admin(**admin_data)
                admins.append(admin)
            return admins