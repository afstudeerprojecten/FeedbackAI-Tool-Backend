from dataclasses import dataclass
from typing import Self
from app.Feedback.Repository.feedbackRepoAsync import FeedbackRepositoryAsync
from app.Feedback.Repository.feedbackRepositoryInterface import IFeedbackRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import CreateFeedback as CreateFeedbackSchema
from app.schemas import Feedback as FeedbackSchema


@dataclass
class FeedbackService:
    
    feedbackRepository: IFeedbackRepository


    @classmethod
    def from_async_repo(cls, session: AsyncSession) -> Self:
        feedbackRepository = FeedbackRepositoryAsync(session=session)

        return FeedbackService(feedbackRepository=feedbackRepository)
