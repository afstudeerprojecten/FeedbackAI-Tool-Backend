from app.Templates.generator.templateGeneratorInterface import ITemplateGenerator
import os
import string
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.Templates.Repository.templateRepositoryInterface import ITemplateRepository
from app.Templates.generator.templateGeneratorInterface import ITemplateGenerator
from app.Assignment.Repository.assignmentRepoAsync import AssignmentRepositoryAsync
from app.Course.Repository.courseRepoAsync import CourseRepositoryAsync
from dataclasses import dataclass

from app.VectorDatabase.Repository.vectorDatabaseInterface import IVectorDatabase
from app.exceptions import EntityNotFoundException

@dataclass
class TemplateGeneratorOpenAI(ITemplateGenerator):

    assignmentRepository: AssignmentRepositoryAsync
    courseRepository: CourseRepositoryAsync

    async def generate_template_solution(self, assignment_id: int, vectorDatabase: IVectorDatabase, organisation_id: int, course_id: int) -> str:
        """
    Generates a template solution for a given assignment ID.

    Args:
        assignment_id (int): The ID of the assignment for which to generate the template solution.

    Returns:
        str: The generated template solution.

    This method generates a template solution for a given assignment by using an AI model
    to simulate a conversation between a teacher and an assistant teacher. The generated
    solution is intended to be used for grading student submissions by comparing them
    to the generated solution.

    The conversation is simulated as follows:
    1. The teacher provides instructions for the assignment.
    2. The assistant teacher generates a solution for the assignment.
    3. The teacher provides feedback on the solution.
    4. The assistant teacher generates another solution based on the feedback, and so on.

    The assignment is delimited by '<start assignment>' and '<end assignment>'.
        """        
        # read assignment
        assignment_repo = self.assignmentRepository
        assignment = await assignment_repo.get_assignment_by_id(assignment_id)
        if (not assignment):
            raise EntityNotFoundException(message=f"Assignment with id {assignment_id} does not exist")

        course_repo = self.courseRepository
        course = await course_repo.get_course_by_id(assignment.course_id)
        if (not course):
            raise EntityNotFoundException(message=f"Course with id {assignment.course_id} does not exist")


        client = AsyncOpenAI()
        aiModel = "gpt-4o"

        uniqueCollectionName: str = vectorDatabase.getUniqueCollectionNameFromIds(organisation_id=organisation_id, course_id=course_id)
        vector_retriever = vectorDatabase.as_retriever(collection_name=uniqueCollectionName, search_k_docs=10)

        # Retrieve relevant context from Chromadb
        relevant_docs = await vector_retriever.ainvoke(assignment.description)
        print("-------got these relevant docs")
        print(relevant_docs)
        relevant_context = "\n\n".join([doc.page_content for doc in relevant_docs])
        print("relevant context stitched together")
        print(relevant_context)

        # Don't change indents for string.Template
        system_message = string.Template("""Hi, I'm a teacher for the course ${course_name}, I want you to act as my assistent teacher. I have an assignment with some instructions.

Now, what I want you to do is generate me some solutions for this assignment. I want to use these template solutions to grade the students' submissions by comparing their submission to all of your solutions, so I can grade them easier and faster. I might even use an AI to compare the stubdents' submissions to generated solutions and let it grade them.

I want you to give me a solution one by one, and each time I'll give feedback to that solution. I'll say wether the solution is good or bad. After that, please send your next solution.

Additionally, you have access to the following relevant context, which consists of text retrieved from the course material of this course. Please use knowledge from the relevant context when generating a solution.
The relevant context is delimited by <start relevantcontext> and <end relevantcontext>. The relevant context is provided below, please read them carefully and understand them:             
<start relevantcontext>      
${relevant_context}
<end relevantcontext>
                                         
The assignment is delimited by <start assignment> and <end assignment>. After reading them, please provide me with your solution. """).substitute(course_name=course.name, relevant_context=relevant_context)

        user_message = string.Template("""Here is the assignment:
<start assignment>
${assignment_title}

${assignment_description}
<end assignment>""").substitute(assignment_title=assignment.title, assignment_description=assignment.description)

        completion = await client.chat.completions.create(
        model=aiModel,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        )

        # return completion
        return completion.choices[0].message.content