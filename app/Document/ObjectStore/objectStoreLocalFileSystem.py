import aiofiles
from app.Document.ObjectStore.objectStoreInterface import IObjectStore
from dataclasses import dataclass
from fastapi import UploadFile
from app.schemas import Course as CourseSchema
from app.schemas import Organisation as OrganisationSchema
import os
from app.vector_database import UPLOADED_FILES_FOLDER


@dataclass
class LocalFileSystemObjectStore(IObjectStore):

    async def saveFile(self, file: UploadFile, organisation: OrganisationSchema, course: CourseSchema) -> str:
        # OVerrides file if already exists for now, no validation yet
        
        # Uploaded files folder path
        uploaded_files_folder = UPLOADED_FILES_FOLDER
        # Create unique folder to save file to, using the organisation and course
        unique_course_folder_name = f"{organisation.name}_{organisation.id}_{course.name}_{course.id}/"
        # Final folder
        out_folder_path = os.path.join(uploaded_files_folder, unique_course_folder_name)
        print(out_folder_path)
        # Create the folder if it doesn't exist
        os.makedirs(out_folder_path, exist_ok=True)

        # Create the full file path
        out_file_path = os.path.join(out_folder_path, file.filename)
        # Save the file to the upload folder
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await file.read(1024):  # async read chunk
                await out_file.write(content)  # async write chunk

        return out_file_path