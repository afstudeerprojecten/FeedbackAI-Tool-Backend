from sqlalchemy.ext.asyncio import AsyncSession
import string
from app.feedbackRepo import FeedbackRepository
from app.models import Submission as SubmissionModel
from app.submissionRepo import SubmissionRepository
from app.schemas import CreateSubmission as CreateSubmissionSchema
from app.schemas import CreateFeedback as CreateFeedbackSchema
from app.schemas import Submission as SubmissionSchema
from app.schemas import Assignment as AssignmentSchema
from app.schemas import Course as CourseSchema
from app.schemas import Template as TemplateSchema
from openai import OpenAI


class SubmissionService:
    session: AsyncSession
    submission_repo: SubmissionRepository

    def __init__(self, session: AsyncSession):
        self.session = session
        self.submission_repo = SubmissionRepository(session=self.session)

    async  def __add_submission(self, submision: CreateSubmissionSchema) -> SubmissionModel:
        submission_repo = SubmissionRepository(session=self.session)
        new_submission = await submission_repo.create_submission(submision, eager_load=True)
        return new_submission
    
    async def student_submit_assignment(self, submission: CreateSubmissionSchema):

        # create de submision
        submission = await self.__add_submission(submission)
        
