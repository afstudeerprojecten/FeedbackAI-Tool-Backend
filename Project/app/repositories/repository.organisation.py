from dataclasses import dataclass    
import app.models as models
from app.database import engine
from app.schemas import CreateOrganisation
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Protocol
from sqlalchemy import Engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OrganisationRepositoryInterface(Protocol):
    def create_organisation(self, organisation: CreateOrganisation) -> models.Organisation:
        ...
    

@dataclass
class OrganisationRepository:
    engine: Engine
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def create_organisation(self, organisation: CreateOrganisation) -> models.Organisation:
        hashed_password = pwd_context.hash(organisation.password)
        with self.engine.connect() as conn:
            conn.execute(
                models.Organisation.__table__.insert().values(
                    name=organisation.name,
                    username=organisation.username,
                    password=hashed_password
                )
            )
            conn.commit()
        return models.Organisation(name=organisation.name, username=organisation.username, password=hashed_password)