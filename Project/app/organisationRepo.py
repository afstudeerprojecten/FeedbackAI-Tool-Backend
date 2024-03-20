from dataclasses import dataclass    
import app.models as models
from app.database import engine
from app.schemas import CreateOrganisation, Organisation
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Protocol, List
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
    
    def get_organisations(self) -> List[Organisation]:
        with self.engine.connect() as conn:
            result = conn.execute(models.Organisation.__table__.select())
            organisations = []
            for row in result.fetchall():
                organisation_data = dict(row._asdict())
                organisation = Organisation(**organisation_data)
                organisations.append(organisation)
            return organisations
        
    def get_organisation_by_name(self, name: str) -> models.Organisation:
        with self.engine.connect() as conn:
            result = conn.execute(
                models.Organisation.__table__.select().where(models.Organisation.name == name)
            )
            return result.fetchone()