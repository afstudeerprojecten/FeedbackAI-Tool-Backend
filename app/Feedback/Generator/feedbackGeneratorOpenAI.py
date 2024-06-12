from dataclasses import dataclass
from app.Feedback.Generator.feedbackGeneratorInterface import IFeedbackGenerator
from app.VectorDatabase.Repository.vectorDatabaseInterface import IVectorDatabase
from app.schemas import Submission as SubmissionSchema
from app.schemas import Template as TemplateSchema
import string
from app.schemas import Assignment as AssignmentSchema
from app.schemas import Course as CourseSchema
from openai import AsyncOpenAI
from openai import ChatCompletion
from langchain_core.vectorstores import VectorStoreRetriever

@dataclass
class FeedbackGeneratorOpenAI(IFeedbackGenerator):
     
     
    async def __create_system_message(self, assignment: AssignmentSchema, course: CourseSchema, template_solutions: list[TemplateSchema], retriever: VectorStoreRetriever) -> str:

        templates = ""

        for template_solution in template_solutions:
            template_out = string.Template("""<start templatesolution>
${solution}
<end templatesolution>

""")
            templates += template_out.substitute(solution=template_solution.content);


        # Retrieve relevant context from Chromadb
        relevant_docs = await retriever.ainvoke(assignment.description, k=13)
        print("-------got these relevant docs")
        print(relevant_docs)
        relevant_context = "\n\n".join([doc.page_content for doc in relevant_docs])
        print("relevant context stitched together")
        print(relevant_context)


        message = string.Template("""You are a teacher at high school for a class of students who are ${age} years old students with a ${background_educational_info}. You teach the course ${course}. You are an expert in the field of ${course}.
You have given an assignment to your students and you will now evaluate and improve their submissions.

Below are the original instructions for the assignment. The assignment is delimited by <start assignment> and <end assignment>. Read these carefully and understand them:

<start assignment>
${assignment_title}
                                  
${assignment_description}
<end assignment>


You will have access to template solutions for this assignment. The template solutions are each delimited by <start templatesolution> and <end templatesolution>. The template solutions are provided below, please read them carefully and understand them:
${template_solutions_expanded}

Use these template solutions to evaluate the student's submission by comparing it to all template solutions and providing feedback relevant to the original assignment.

The student does not have access to the template solutions and should not be aware of their existence. Keep them confidential and do not mention them.
                                  
Additionally, you have access to the following relevant context, retrieved from the course material of this course:
${relevant_context}

Below is the submission of the student's work. Please read it carefully and understand it. Then, provide feedback to the student. The submission is delimited by <start submission> and <end submission>.

Keep the feedback you provide concise. The student will use the feedback to improve their own submission and will later resubmit it here. Do not finish the assignment for the students yourself. Keep the feedback simple and provide only hints. Do not add your own examples to your feedback or sentences like "such as...", the student should come up with examples themselves.

This will be a learning moment for the student. The goal is for the student to improve in the subject ${course}.""")
        
        message = message.substitute(age=assignment.student_ages, background_educational_info="a reasonable STEM education", course=course.name, assignment_title=assignment.title, assignment_description=assignment.description, template_solutions_expanded=templates, relevant_context=relevant_context)

        return message
    

    async def __create_user_message(self, submission: SubmissionSchema) -> str:
        user_message = string.Template("""This is the student's latest submission:
<start submission>
${submission}
<end submission>""")
        
        return user_message.substitute(submission=submission.content)


    async def generate_feedback(self, submission: SubmissionSchema, vectorDatabase: IVectorDatabase, organisation_id: int, course_id: int) -> ChatCompletion:

        uniqueCollectionName: str = vectorDatabase.getUniqueCollectionNameFromIds(organisation_id=organisation_id, course_id=course_id)
        vector_retriever = vectorDatabase.as_retriever(collection_name=uniqueCollectionName, search_k_docs=15)
    
        system_message = await self.__create_system_message(submission.assignment, submission.assignment.course, submission.assignment.templates, vector_retriever)

        print("+++++++++ system message\n"+system_message)

        user_message = await self.__create_user_message(submission)
        print("+++++++++ user message\n"+user_message)

        client = AsyncOpenAI()

        aiModel = "gpt-4o"	

        completion = await client.chat.completions.create(
            model=aiModel,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        
        return completion