from typing import Protocol
from app.schemas import Submission as SubmissionSchema
from openai import ChatCompletion

class IFeedbackGenerator(Protocol):
        
    async def generate_feedback(self, submission: SubmissionSchema) -> ChatCompletion:
        ...