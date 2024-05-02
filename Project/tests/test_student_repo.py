import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import pytest_asyncio
from sqlalchemy.orm import sessionmaker
from app.studentRepo import StudentRepository
from app.models import Organisation, Teacher, Student
from app.schemas import CreateStudent

@pytest.fixture
async def async_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession, future=True
    )
    session = async_session()
    try:
        return session
    finally:
        await session.close()

@pytest.fixture
async def student_repo(async_session: AsyncSession) -> StudentRepository:
    session = async_session()
    try:
        student_repository = StudentRepository(session=session)
        return student_repository
    finally:
        await session.close()

@pytest.mark.asyncio
async def test_create_student(student_repo: StudentRepository):
    print(f"+++++++++++++++++++++++++++++++++++{type(student_repo)}+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    create_student_data = CreateStudent(
        name="John",
        lastname="Doe",
        email="john.doe@example.com",
        password="password123",
        organisation_id=1,
    )
    created_student = await student_repo.create_student(create_student_data)

    assert created_student.name == "John"
    assert created_student.lastname == "Doe"
    assert created_student.email == "john.doe@example.com"
    assert created_student.organisation_id == 1
