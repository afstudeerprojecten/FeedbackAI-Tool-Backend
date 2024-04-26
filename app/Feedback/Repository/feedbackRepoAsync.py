from sqlalchemy.ext.asyncio import AsyncSession
from app.Feedback.Repository.feedbackRepositoryInterface import IFeedbackRepository
from app.schemas import CreateFeedback as CreateFeedbackSchema
from app.schemas import Feedback as FeedbackSchema
from app.models import Submission as SubmissionModel
from app.models import Feedback as FeedbackModel
from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only


@dataclass
class FeedbackRepositoryAsync(IFeedbackRepository):

    session: AsyncSession


    async def create_feedback(self, feedback: CreateFeedbackSchema) -> FeedbackSchema:
        new_feedback = FeedbackModel(submission_id=feedback.submission_id, content=feedback.content)
        self.session.add(new_feedback)
        await self.session.commit()

        await self.session.refresh(new_feedback)
        feedback_validated = FeedbackSchema.model_validate(new_feedback)
        return feedback_validated
    
    async def get_feedback_by_submission_id(self, submission_id: int) -> FeedbackSchema:
        query = select(FeedbackModel).where(FeedbackModel.submission_id == submission_id)
        result = await self.session.execute(query)
        feedback = result.scalars().first()
        feedback_validated = FeedbackSchema.model_validate(feedback)
        return feedback_validated