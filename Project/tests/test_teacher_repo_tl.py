import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.teacherRepo import TeacherRepository
from app.schemas import CreateTeacher, UpdateTeacher
from app.models import Teacher
from app.database import Base

# Create an in-memory SQLite database for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create the engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

@pytest.fixture(autouse=True, scope="module")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture
async def session():
    async with async_session() as session:
        yield session

@pytest.fixture
async def teacher_repo(session):
    async with session.begin():
        yield TeacherRepository(session)

@pytest.mark.asyncio
async def test_create_teacher(teacher_repo):
    teacher_data = CreateTeacher(
        name="John",
        lastname="Doe",
        email="john.doe@example.com",
        password="password123",
        organisation_id=1
    )
    teacher = await teacher_repo.create_teacher(teacher_data)
    assert teacher.name == "John"
    assert teacher.lastname == "Doe"
    assert teacher.email == "john.doe@example.com"

@pytest.mark.asyncio
async def test_get_teachers(teacher_repo):
    # Ensure there are no teachers initially
    teachers = await teacher_repo.get_teachers()
    assert len(teachers) == 0

    # Create a teacher
    teacher_data = CreateTeacher(
        name="Jane",
        lastname="Smith",
        email="jane.smith@example.com",
        password="password123",
        organisation_id=1
    )
    await teacher_repo.create_teacher(teacher_data)

    # Retrieve teachers and check if the created teacher exists
    teachers = await teacher_repo.get_teachers()
    assert len(teachers) == 1
    assert teachers[0].name == "Jane"

@pytest.mark.asyncio
async def test_get_teacher_by_id(teacher_repo):
    # Create a teacher
    teacher_data = CreateTeacher(
        name="Jane",
        lastname="Smith",
        email="jane.smith@example.com",
        password="password123",
        organisation_id=1
    )
    teacher = await teacher_repo.create_teacher(teacher_data)

    # Retrieve the teacher by ID
    retrieved_teacher = await teacher_repo.get_teacher_by_id(teacher.id)
    assert retrieved_teacher.name == "Jane"

@pytest.mark.asyncio
async def test_delete_teacher_by_id(teacher_repo):
    # Create a teacher
    teacher_data = CreateTeacher(
        name="Jane",
        lastname="Smith",
        email="jane.smith@example.com",
        password="password123",
        organisation_id=1
    )
    teacher = await teacher_repo.create_teacher(teacher_data)

    # Delete the teacher by ID
    await teacher_repo.delete_teacher_by_id(teacher.id)

    # Ensure the teacher is deleted
    retrieved_teacher = await teacher_repo.get_teacher_by_id(teacher.id)
    assert retrieved_teacher is None

@pytest.mark.asyncio
async def test_update_teacher(teacher_repo):
    # Create a teacher
    teacher_data = CreateTeacher(
        name="Jane",
        lastname="Smith",
        email="jane.smith@example.com",
        password="password123",
        organisation_id=1
    )
    teacher = await teacher_repo.create_teacher(teacher_data)

    # Update the teacher
    update_data = UpdateTeacher(name="Jane Updated")
    updated_teacher = await teacher_repo.update_teacher(teacher.id, update_data)

    # Ensure the teacher is updated
    assert updated_teacher.name == "Jane Updated"
