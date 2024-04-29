from typing import Protocol
from app.schemas import Submission as SubmissionSchema

class IFeedbackGenerator(Protocol):
        
    async def generate_feedback(self, submission: SubmissionSchema) -> str:
        ...