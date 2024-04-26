from sqlalchemy.ext.asyncio import AsyncSession
from app.Submission.Repository.submissionRepositoryInterface import ISubmissionRepository
from app.schemas import CreateSubmission as CreateSubmissionSchema
from app.schemas import Submission as SubmissionSchema
from app.models import Submission as SubmissionModel
from app.models import Assignment as AssignmentModel
from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only


@dataclass
class SubmissionRepositoryAsync(ISubmissionRepository):
    session: AsyncSession

    async def create_submission(self, submision: CreateSubmissionSchema, eager_load: bool=False) -> SubmissionSchema:
        new_submission = SubmissionModel(assignment_id=submision.assignment_id, student_id=submision.student_id, content=submision.content)
        self.session.add(new_submission)
        await self.session.commit()
        
        await self.session.refresh(new_submission)

        # Make query
        query = select(SubmissionModel)
        # Manually eager load the related objects, if specified
        if eager_load:
            query = query.options(
                joinedload(SubmissionModel.assignment).options(
                    joinedload(AssignmentModel.templates),
                    joinedload(AssignmentModel.course)
                ),
                joinedload(SubmissionModel.student), 
                joinedload(SubmissionModel.feedback))
        query = query.where(SubmissionModel.id == new_submission.id)

        result = await self.session.execute(query)

        submissionValidated = SubmissionSchema.model_validate(result.scalars().first())
        return submissionValidated
    
    async def get_all_submissions(self) -> list[SubmissionSchema]:

        query = select(SubmissionModel)

        print(query)
        result = await self.session.execute(query)
        result = result.unique()        

        submissions = []
        for submission in result.scalars():
    		# Set assignment, student, and feedback to None before validation
            # OTHERWISE ASYNC ERRORS
            submission.assignment = None
            submission.student = None
            submission.feedback = None
            submissions.append(SubmissionSchema.model_validate(submission))

        # submissions = [SubmissionSchema.model_validate(submission) for submission in result.scalars()]
        return submissions
    

    async def get_submission_by_id(self, submission_id: int) -> SubmissionSchema:
        query = select(SubmissionModel).where(SubmissionModel.id == submission_id)
        result = await self.session.execute(query)
        submission = result.scalars().first()
        submission.assignment = None
        submission.student = None
        submission.feedback = None
        return SubmissionSchema.model_validate(submission)