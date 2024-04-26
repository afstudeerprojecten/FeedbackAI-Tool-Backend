from app.schemas import CreateSubmission as CreateSubmissionSchema
from app.schemas import Submission as SubmissionSchema
from typing import Protocol


class ISubmissionRepository(Protocol):

    async def create_submission(self, submision: CreateSubmissionSchema, eager_load: bool=False) -> SubmissionSchema:
        ...

    async def get_all_submissions(self) -> list[SubmissionSchema]:
        ...

    async def get_submission_by_id(self, submission_id: int) -> SubmissionSchema:
        ...