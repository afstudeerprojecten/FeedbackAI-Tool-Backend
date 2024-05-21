# Project/tests/test_submissionRepo.py

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from app.models import Base, Submission, Assignment, Student, Feedback
from app.schemas import CreateSubmission, Submission as SubmissionSchema
from app.submissionRepo import SubmissionRepository


@pytest.fixture
async def db_session():
    # Set up an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        yield async_session()
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def submission_repository(db_session):
    async with db_session() as session:
        async with session.begin():
            yield SubmissionRepository(session)


@pytest.mark.asyncio
async def test_create_submission(submission_repository: SubmissionRepository):
    # Create a submission
    submission_data = CreateSubmission(
        assignment_id=1,
        student_id=1,
        content="This is a test submission.",
    )
    created_submission = await submission_repository.create_submission(submission_data)
    assert created_submission.id is not None
    assert created_submission.assignment_id == 1
    assert created_submission.student_id == 1
    assert created_submission.content == "This is a test submission."


@pytest.mark.asyncio
async def test_get_all_submissions(submission_repository: SubmissionRepository):
    # Create some submissions
    submission_data_1 = CreateSubmission(
        assignment_id=1,
        student_id=1,
        content="This is submission 1.",
    )
    submission_data_2 = CreateSubmission(
        assignment_id=2,
        student_id=2,
        content="This is submission 2.",
    )
    await submission_repository.create_submission(submission_data_1)
    await submission_repository.create_submission(submission_data_2)

    # Retrieve all submissions
    submissions = await submission_repository.get_all_submissions()
    assert len(submissions) == 2
    assert submissions[0].content == "This is submission 1."
    assert submissions[1].content == "This is submission 2."


@pytest.mark.asyncio
async def test_get_submission_by_id(submission_repository: SubmissionRepository):
    # Create a submission
    submission_data = CreateSubmission(
        assignment_id=1,
        student_id=1,
        content="This is a test submission.",
    )
    created_submission = await submission_repository.create_submission(submission_data)

    # Retrieve the submission by ID
    retrieved_submission = await submission_repository.get_submission_by_id(
        created_submission.id
    )
    assert retrieved_submission is not None
    assert retrieved_submission.id == created_submission.id
    assert retrieved_submission.assignment_id == 1
    assert retrieved_submission.student_id == 1
    assert retrieved_submission.content == "This is a test submission."
