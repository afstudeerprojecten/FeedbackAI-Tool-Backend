from typing import Optional, Protocol
from app.schemas import CreateFeedback as CreateFeedbackSchema
from app.schemas import Feedback as FeedbackSchema


class IFeedbackRepository(Protocol):
    
    async def create_feedback(self, feedback: CreateFeedbackSchema) -> FeedbackSchema:
        ...
    
    async def get_feedback_by_submission_id(self, submission_id: int) -> Optional[FeedbackSchema]:
        ...