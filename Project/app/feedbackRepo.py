from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import CreateFeedback as CreateFeedbackSchema
from app.schemas import Feedback as FeedbackSchema
from app.models import Submission as SubmissionModel
from app.models import Feedback as FeedbackModel
from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only


@dataclass
class FeedbackRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def create_feedback(self, feedback: CreateFeedbackSchema) -> FeedbackSchema:
        new_feedback = FeedbackModel(submission_id=feedback.submission_id, content=feedback.content)
        self.session.add(new_feedback)
        await self.session.commit()

        await self.session.refresh(new_feedback)
        feedback_validated = FeedbackSchema.model_validate(new_feedback)
        return feedback_validated