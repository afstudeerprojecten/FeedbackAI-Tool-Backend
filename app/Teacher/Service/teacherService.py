from app.models import Teacher
from app.schemas import CreateTeacher, Teacher as StudentSchema, UpdateTeacher
from app.Teacher.Repository.teacherRepo import InterfaceTeacherRepository


class TeacherAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name

class TeacherNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

class TeacherIdNotFoundException(Exception):
    def __init__(self, teacher_id: int):
        self.teacher_id = teacher_id

class NoTeachersFoundException(Exception):
    def __init__(self):
        pass

class TeacherService():
    def __init__(self, teacher_repo: InterfaceTeacherRepository):
        self.teacher_repo = teacher_repo
    async def create_teacher(self, teacher: CreateTeacher):
        if await self.teacher_repo.get_teacher_by_email(teacher.email):
            raise TeacherAlreadyExistsException(teacher.email)
        else:
            await self.teacher_repo.create_teacher(teacher)
            return {"message": "Teacher created successfully"}

        
    async def get_teachers(self):
        if await self.teacher_repo.get_teachers() == []:
            raise NoTeachersFoundException()
        else:
            teachers = await self.teacher_repo.get_teachers()
            return teachers
       
    async def get_teacher_by_firstname(self, name: str):
        teacher = await self.teacher_repo.get_teacher_by_firstname(name)
        if teacher is None:
            raise TeacherNotFoundException(name)
        return teacher

    
    async def get_teacher_by_id(self, teacher_id: int):
        if not await self.teacher_repo.get_teacher_by_id(teacher_id):
            raise TeacherIdNotFoundException(teacher_id)
        else:
            teacher = await self.teacher_repo.get_teacher_by_id(teacher_id)
            return teacher
        
    async def delete_teacher(self, teacher_id: int):
        if not await self.teacher_repo.get_teacher_by_id(teacher_id):
            raise TeacherIdNotFoundException(teacher_id)
        else:
            await self.teacher_repo.delete_teacher_by_id(teacher_id)
            return {"message": "Teacher deleted successfully"}
        
    async def update_teacher(self, teacher_id: int, teacher_data: UpdateTeacher):
        if not await self.teacher_repo.get_teacher_by_id(teacher_id):
            raise TeacherIdNotFoundException(teacher_id)
        else:
            teacher = await self.teacher_repo.update_teacher(teacher_id, teacher_data)
            return teacher
        
    async def get_teacher_by_email(self, email: str):
        teacher = await self.teacher_repo.get_teacher_by_email(email)
        if teacher:
            return teacher
        else:
            None