from typing import Protocol
from app.VectorDatabase.Repository.vectorDatabaseInterface import IVectorDatabase
from app.schemas import Submission as SubmissionSchema
from openai import ChatCompletion

class IFeedbackGenerator(Protocol):
        
    async def generate_feedback(self, submission: SubmissionSchema, vectorDatabase: IVectorDatabase, organisation_id: int, course_id: int) -> ChatCompletion:
        ...