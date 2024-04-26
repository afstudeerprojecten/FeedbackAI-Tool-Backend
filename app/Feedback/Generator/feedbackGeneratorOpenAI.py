from attr import dataclass
from app.Feedback.Generator.feedbackGeneratorInterface import IFeedbackGenerator
from app.schemas import Submission as SubmissionSchema

@dataclass
class FeedbackGeneratorOpenAI(IFeedbackGenerator):

     async def generate_feedback(self, submission: SubmissionSchema) -> str:
        ...