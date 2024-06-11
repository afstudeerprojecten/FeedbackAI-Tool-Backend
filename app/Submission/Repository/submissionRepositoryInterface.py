from app.schemas import CreateSubmission as CreateSubmissionSchema
from app.schemas import Submission as SubmissionSchema
from typing import Optional, Protocol


class ISubmissionRepository(Protocol):

    async def create_submission(self, submision: CreateSubmissionSchema, eager_load: bool=True) -> SubmissionSchema:
        ...

    async def get_all_submissions(self) -> list[SubmissionSchema]:
        ...

    async def get_submission_by_id(self, submission_id: int) -> Optional[SubmissionSchema]:
        ...

    async def get_submissions_by_student_id(self, student_id: int) -> list[SubmissionSchema]:
        ...