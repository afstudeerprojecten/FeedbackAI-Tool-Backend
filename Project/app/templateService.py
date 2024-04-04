import os
import string
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.assignmentRepo import AssignmentRepository
from app.courseRepo import CourseRepository


class TemplateService:

    session: AsyncSession


    def __init__(self, session: AsyncSession):
        self.session = session

    async def generate_template_solution(self, assignment_id: int) -> str:

        # read assignment
        assignment_repo = AssignmentRepository(session=self.session)
        assignment = await assignment_repo.get_assignment_by_id(assignment_id)

        course_repo = CourseRepository(session=self.session)
        course = await course_repo.get_course_by_id(assignment.course_id)


        openai_api_key=os.getenv('OPENAI_API_KEY', 'YourAPIKey') 
        client = OpenAI()
        aiModel = "gpt-4-turbo-preview"


        # Don't change indents for string.Template
        system_message = string.Template("""Hi, I'm a teacher for the course ${course_name}, I want you to act as my assistent teacher. I have an assignment with some instructions.

Now, what I want you to do is generate me some solutions for this assignment. I want to use these template solutions to grade the students' submissions by comparing their submission to all of your solutions, so I can grade them easier and faster. I might even use an AI to compare the stubdents' submissions to generated solutions and let it grade them.

I want you to give me a solution one by one, and each time I'll give feedback to that solution. I'll say wether the solution is good or bad. After that, please send your next solution.

The assignment is delimited by <start assignment> and <end assignment>. After reading them, please provide me with your solution. """).substitute(course_name=course.name)
        
        user_message = string.Template("""Here is the assignment:
<start assignment>
${assignment_title}

${assignment_description}
<end assignment>""").substitute(assignment_title=assignment.title, assignment_description=assignment.description)

        completion = client.chat.completions.create(
        model=aiModel,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        )

        # return completion
        return completion.choices[0].message.content
