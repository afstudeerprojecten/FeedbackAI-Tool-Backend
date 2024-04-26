from dataclasses import dataclass
from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession
import string
from app.Feedback.Generator.feedbackGeneratorInterface import IFeedbackGenerator
from app.Feedback.Generator.feedbackGeneratorOpenAI import FeedbackGeneratorOpenAI
from app.Feedback.Repository.feedbackRepositoryInterface import IFeedbackRepository
from app.Submission.Repository.submissionRepositoryInterface import ISubmissionRepository
from app.Feedback.Repository.feedbackRepoAsync import FeedbackRepositoryAsync
from app.models import Submission as SubmissionModel
from app.Submission.Repository.submissionRepoAsync import SubmissionRepositoryAsync
from app.schemas import CreateSubmission as CreateSubmissionSchema
from app.schemas import CreateFeedback as CreateFeedbackSchema
from app.schemas import Submission as SubmissionSchema
from app.schemas import Assignment as AssignmentSchema
from app.schemas import Course as CourseSchema
from app.schemas import Template as TemplateSchema
from openai import OpenAI

@dataclass
class SubmissionService:
    submissionRepository: ISubmissionRepository
    feedbackGenerator: IFeedbackGenerator
    feedbackRepository: IFeedbackRepository

    @classmethod
    def from_async_repo_and_open_ai_feedback_generator(cls, session: AsyncSession) -> Self:
        submissionRepository = SubmissionRepositoryAsync(session)
        feedbackGenerator = FeedbackGeneratorOpenAI()
        feedbackRepository = FeedbackRepositoryAsync(session=session)

        return SubmissionService(submissionRepository=submissionRepository, feedbackGenerator=feedbackGenerator, feedbackRepository=feedbackRepository)


    async  def __add_submission(self, submision: CreateSubmissionSchema) -> SubmissionModel:
        return await self.submissionRepository.create_submission(submision, eager_load=True)


    async def __generate_feedback(self, submission: SubmissionSchema) -> str:
        return await self.feedbackGenerator.generate_feedback(submission=submission)


    async def student_submit_assignment(self, submission: CreateSubmissionSchema):

        # create de submision
        submission = await self.__add_submission(submission)
        
        feedback_chat_completion = await self.__generate_feedback(submission)

        feedback = CreateFeedbackSchema(submission_id=submission.id, content=feedback_chat_completion.content)
        new_feedback = await self.feedbackRepository.create_feedback(feedback=feedback)

        return new_feedback