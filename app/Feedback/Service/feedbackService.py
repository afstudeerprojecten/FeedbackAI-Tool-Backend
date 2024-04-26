from dataclasses import dataclass
from typing import Self
from app.Feedback.Repository.feedbackRepoAsync import FeedbackRepositoryAsync
from app.Feedback.Repository.feedbackRepositoryInterface import IFeedbackRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.Submission.Repository.submissionRepoAsync import SubmissionRepositoryAsync
from app.Submission.Repository.submissionRepositoryInterface import ISubmissionRepository
from app.exceptions import EntityNotFoundException
from app.schemas import CreateFeedback as CreateFeedbackSchema
from app.schemas import Feedback as FeedbackSchema


@dataclass
class FeedbackService:
    
    feedbackRepository: IFeedbackRepository
    submissionRepository: ISubmissionRepository

    @classmethod
    def from_async_repo(cls, session: AsyncSession) -> Self:
        feedbackRepository = FeedbackRepositoryAsync(session=session)
        submissionRepository = SubmissionRepositoryAsync(session=session)

        return FeedbackService(feedbackRepository=feedbackRepository, submissionRepository=submissionRepository)


    async def create_feedback(self, feedback: CreateFeedbackSchema) -> FeedbackSchema:
        return await self.feedbackRepository.create_feedback(feedback=feedback)
    
    async def get_feedback_by_submission_id(self, submission_id: int) -> FeedbackSchema:
        return await self.feedbackRepository.get_feedback_by_submission_id(submission_id=submission_id)
