import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from app.models import Base, Submission, Assignment, Student, Feedback
from app.schemas import CreateSubmission, Submission as SubmissionSchema
from app.submissionRepo import SubmissionRepository
from app.feedbackRepo import FeedbackRepository
from app.submissionService import SubmissionService


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
async def submission_service(db_session):
    async with db_session() as session:
        async with session.begin():
            yield SubmissionService(session)


@pytest.mark.asyncio
async def test_student_submit_assignment(submission_service: SubmissionService):
    # Create a submission
    submission_data = CreateSubmission(
        assignment_id=1,
        student_id=1,
        content="This is a test submission.",
    )
    new_feedback = await submission_service.student_submit_assignment(submission_data)
    
    assert new_feedback.id is not None
    assert new_feedback.submission_id == 1
    assert "AI-generated feedback" in new_feedback.content  # Just a placeholder