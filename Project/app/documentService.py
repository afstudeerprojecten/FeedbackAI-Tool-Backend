from fastapi import UploadFile
import aiofiles
import os
from app.courseRepo import CourseRepository
from app.teacherRepo import TeacherRepository

class DocumentService:
    session: AsyncSession
    teacher_repo: TeacherRepository
    course_repo: CourseRepository

    def __init__(self, session: AsyncSession):
        self.session = session
        self.teacher_repo = TeacherRepository(session=session) 
        self.course_repo = CourseRepository(session=session)

    async def uploadDocument(
        self,  
        teacher_id: int,
        course_id: int,
        file: UploadFile ):

        # Save file locally
        out_file_path = await self.__saveFileLocally(file=file)

        return {"message": "file written out"}
    

    async def __saveFileLocally(self, file: UploadFile):
        # Uploaded files folder path
        uploaded_files_folder = "./uploaded_files/"

        # Create the folder if it doesn't exist
        os.makedirs(uploaded_files_folder, exist_ok=True)

        # Save the file to the upload folder
        out_file_path = os.path.join(uploaded_files_folder, file.filename)

        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await file.read(1024):  # async read chunk
                await out_file.write(content)  # async write chunk

        return out_file_path
