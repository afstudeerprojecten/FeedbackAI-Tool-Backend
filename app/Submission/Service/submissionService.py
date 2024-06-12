from dataclasses import dataclass
from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession
import string
from app.Assignment.Repository.assignmentRepoAsync import AssignmentRepositoryAsync
from app.Assignment.Repository.assignmentRepositoryInterface import IAssignmentRepository
from app.Embedding.Generator.embeddingGeneratorInterface import IEmbeddingGenerator
from app.Embedding.Generator.openAIEmbeddingGenerator import OpenAIEmbeddingGenerator
from app.Feedback.Generator.feedbackGeneratorInterface import IFeedbackGenerator
from app.Feedback.Generator.feedbackGeneratorOpenAI import FeedbackGeneratorOpenAI
from app.Feedback.Repository.feedbackRepositoryInterface import IFeedbackRepository
from app.Student.Repository.studentRepo import InterfaceStudentRepository, StudentRepository
from app.Submission.Repository.submissionRepositoryInterface import ISubmissionRepository
from app.Feedback.Repository.feedbackRepoAsync import FeedbackRepositoryAsync
from app.VectorDatabase.Repository.ChromaVectorDatabase import ChromaVectorDatabase
from app.VectorDatabase.Repository.vectorDatabaseInterface import IVectorDatabase
from app.exceptions import EntityNotFoundException
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
    assignmentRepository: IAssignmentRepository
    studentRepository: InterfaceStudentRepository
    vectorDatabase: IVectorDatabase

    @classmethod
    def from_async_repo_and_open_ai_feedback_generator(cls, session: AsyncSession) -> Self:
        submissionRepository = SubmissionRepositoryAsync(session)
        feedbackGenerator = FeedbackGeneratorOpenAI()
        feedbackRepository = FeedbackRepositoryAsync(session=session)
        assignmentRepository = AssignmentRepositoryAsync(session=session)
        studentRepository = StudentRepository(session=session)
        embeddingGenerator = OpenAIEmbeddingGenerator()
        vectorDatabase = ChromaVectorDatabase(embedding_generator=embeddingGenerator)


        return SubmissionService(submissionRepository=submissionRepository, feedbackGenerator=feedbackGenerator, feedbackRepository=feedbackRepository, assignmentRepository=assignmentRepository, studentRepository=studentRepository, vectorDatabase=vectorDatabase)


    async  def __add_submission(self, submision: CreateSubmissionSchema) -> SubmissionModel:
        return await self.submissionRepository.create_submission(submision, eager_load=True)


    async def __generate_feedback(self, submission: SubmissionSchema) -> str:
        return await self.feedbackGenerator.generate_feedback(submission=submission)


    async def student_submit_assignment(self, submission: CreateSubmissionSchema):

        #check of assignment id echt is
        assignment = await self.assignmentRepository.get_assignment_by_id(assignment_id=submission.assignment_id, eager_load=True)
        if (not assignment):
            raise EntityNotFoundException(message=f"Assignment with id {submission.assignment_id} does not exist")
        else:
            # check of de student id echt is
            student = await self.studentRepository.get_student_by_id(student_id=submission.student_id)
            if (not student):
                raise EntityNotFoundException(message=f"Student with id {submission.student_id} does not exist")
            else:
                # create de submision
                submission = await self.__add_submission(submission)
                
                feedback_chat_completion = await self.__generate_feedback(submission)
                print(feedback_chat_completion)
                print(feedback_chat_completion.usage.total_tokens)
                
                feedback = CreateFeedbackSchema(submission_id=submission.id, content=feedback_chat_completion.choices[0].message.content)
                new_feedback = await self.feedbackRepository.create_feedback(feedback=feedback)

                return {'feedback': new_feedback, 'usage_total_tokens': feedback_chat_completion.usage.total_tokens}
    
    async def get_all_submissions(self) -> list[SubmissionSchema]:
        return await self.submissionRepository.get_all_submissions()
    

    async def get_submission_by_id(self, submission_id: int) -> SubmissionSchema:
        submission = await self.submissionRepository.get_submission_by_id(submission_id=submission_id)
        if (not submission):
            raise EntityNotFoundException(message=f"Submission with id {submission_id} does not exist")
        else:
            return submission
        
    async def get_submissions_by_student_id(self, student_id: int) -> list[SubmissionSchema]:
        submission = await self.submissionRepository.get_submissions_by_student_id(student_id=student_id)
        if (not submission):
            raise EntityNotFoundException(message=f"Submission with student id {student_id} does not exist")
        else:
            return submission