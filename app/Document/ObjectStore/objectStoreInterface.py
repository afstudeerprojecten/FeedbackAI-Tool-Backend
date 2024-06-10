from typing import Protocol

from fastapi import UploadFile

from app.models import Course as CourseSchema
from app.schemas import Organisation as OrganisationSchema

class IObjectStore(Protocol):

    async def saveFile(self, file: UploadFile, organisation: OrganisationSchema, course: CourseSchema) -> str:
        ...