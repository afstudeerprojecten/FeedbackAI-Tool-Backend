from app.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from app.models import Teacher
from app.schemas import CreateTeacher, Teacher as StudentSchema, UpdateTeacher
from app.Teacher.Repository.teacherRepo import InterfaceTeacherRepository


class TeacherService():
    def __init__(self, teacher_repo: InterfaceTeacherRepository):
        self.teacher_repo = teacher_repo

    async def create_teacher(self, teacher: CreateTeacher):
        if await self.teacher_repo.get_teacher_by_emailCheck(teacher.email):
            raise EntityAlreadyExistsException(f"Teacher with email {teacher.email} already exists")
        else:
            await self.teacher_repo.create_teacher(teacher)
            return {"message": "Teacher created successfully"}

    async def get_teachers(self):
        if await self.teacher_repo.get_teachers() == []:
            raise EntityNotFoundException("No teachers found")
        else:
            teachers = await self.teacher_repo.get_teachers()
            return teachers

    async def get_teacher_by_firstname(self, name: str):
        teacher = await self.teacher_repo.get_teacher_by_firstname(name)
        if teacher is None:
            raise EntityNotFoundException(f"Teacher with name {name} not found")
        return teacher

    async def get_teacher_by_id(self, teacher_id: int):
        if not await self.teacher_repo.get_teacher_by_id(teacher_id):
            raise EntityNotFoundException(f"Teacher with ID {teacher_id} not found")
        else:
            teacher = await self.teacher_repo.get_teacher_by_id(teacher_id)
            return teacher

    async def delete_teacher(self, teacher_id: int):
        if not await self.teacher_repo.get_teacher_by_id(teacher_id):
            raise EntityNotFoundException(f"Teacher with ID {teacher_id} not found")
        else:
            await self.teacher_repo.delete_teacher_by_id(teacher_id)
            return {"message": "Teacher deleted successfully"}

    async def update_teacher(self, teacher_id: int, teacher_data: UpdateTeacher):
        if not await self.teacher_repo.get_teacher_by_id(teacher_id):
            raise EntityNotFoundException(f"Teacher with ID {teacher_id} not found")
        else:
            teacher = await self.teacher_repo.update_teacher(teacher_id, teacher_data)
            return teacher

    async def get_teacher_by_emailCheck(self, email: str):
        teacher = await self.teacher_repo.get_teacher_by_email(email)
        if teacher:
            return teacher
        else:
            return None

    async def get_teacher_by_email(self, email: str):
        teacher = await self.teacher_repo.get_teacher_by_email(email)
        if teacher is None:
            raise EntityNotFoundException(f"Teacher with email {email} not found")
        return teacher