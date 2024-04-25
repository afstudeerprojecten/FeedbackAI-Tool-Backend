from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.Assignment.Service.assignmentService import AssignmentService
from app.Course.Service.courseService import CourseService
from app.Templates.Service.templateService import TemplateService
from app.submissionRepo import SubmissionRepository
from app.submissionService import SubmissionService
from app.Templates.Repository.templateRepoAsync import TemplateRepositoryAsync
from app.database import async_engine, SessionLocal as async_session
from app.organisationRepo import OrganisationRepository
from app.adminRepo import AdminRepository
from app.Course.Repository.courseRepoAsync import CourseRepositoryAsync
from app.teacherRepo import TeacherRepository
from app.studentRepo import StudentRepository
from app.feedbackRepo import FeedbackRepository
from app.organisationService import OrganisationService, AlreadyExistsException, NotExistsException, NotExistsIdException, NoOrganisationsFoundException
from app.studentService import StudentService, StudentAlreadyExistsException, StudentNotFoundException, StudentIdNotFoundException, NoStudentsFoundException
from app.schemas import CreateTemplate, Organisation, CreateOrganisation, CreateAdmin, CreateTeacher, CreateCourse, CreateAssignment, UpdateTeacher, CreateSubmission, CreateStudent
import asyncio
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware
from app.Assignment.Repository.assignmentRepoAsync import AssignmentRepositoryAsync
from dotenv import load_dotenv
import os


load_dotenv()
openai_api_key=os.getenv('OPENAI_API_KEY', 'YourAPIKey')

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_async_db():
    async with async_session() as session:
        yield session


# No need for db_dependency annotation
def db_dependency():
    return Depends(get_async_db)


@app.get("/")
async def root():
    return {"message": "Welcome to the API, made with FastAPI!!"}


@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": f"Organisation with name '{exc.name}' already exists"},
    )

@app.exception_handler(NotExistsException)
async def not_exists_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Organisation with name '{exc.name}' does not exist"},
    )

@app.exception_handler(NotExistsIdException)
async def not_exists_id_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Organisation with ID '{exc.organisation_id}' does not exist"},
    )

@app.exception_handler(NoOrganisationsFoundException)
async def no_organisations_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "No organisations found"},
    )

@app.exception_handler(StudentAlreadyExistsException)
async def student_already_exists_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": f"Student with name '{exc.name}' already exists"},
    )

@app.exception_handler(StudentNotFoundException)
async def student_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Student with name '{exc.name}' does not exist"},
    )

@app.exception_handler(StudentIdNotFoundException)
async def student_id_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Student with ID '{exc.student_id}' does not exist"},
    )

@app.exception_handler(NoStudentsFoundException)
async def no_students_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "No students found"},
    )



# ORGANISATION
@app.post("/organisation/add", status_code=status.HTTP_201_CREATED)
async def create_organisation(organisation: CreateOrganisation, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new organisation.

    Args:
        organisation (CreateOrganisation): The details of the organisation to be created.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the organisation is created successfully.

    Raises:
        HTTPException: If there is an error creating the organisation.
    """
    repo = OrganisationRepository(session=db)
    service = OrganisationService(repo)
    existing_organisation = await service.get_organisation_by_name(organisation.name)
    if existing_organisation:
        raise AlreadyExistsException(organisation.name)
    else:
        await service.create_organisation(organisation)
        return {"message": "Organisation created successfully"}
    
@app.get("/organisations")
async def get_organisations(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a list of organisations from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[Organisation] - A list of organisations retrieved from the database.

    Raises:
    - HTTPException: If there is an error retrieving the organisations from the database.
    """
    repo = OrganisationRepository(session=db)
    service = OrganisationService(repo)
    if not await service.get_organisations():
        raise NoOrganisationsFoundException()
    else:
        return await service.get_organisations()

@app.get("/organisation/{name}")
async def get_organisation_by_name(name: str, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve an organisation by its name.

    Args:
        name (str): The name of the organisation.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        dict: The organisation details if found.

    Raises:
        HTTPException: If the organisation is not found or an error occurs.
    """
    repo = OrganisationRepository(session=db)
    service = OrganisationService(repo)
    if not await service.get_organisation_by_name(name):
        raise NotExistsException(name)
    else:
       return await service.get_organisation_by_name(name)
    

 

@app.get("/organisation/id/{id}")
async def get_organisation_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve an organisation by its ID.

    Parameters:
    - id (int): The ID of the organisation to retrieve.
    - db (AsyncSession): The asynchronous database session.

    Returns:
    - dict: The organisation information if found.

    Raises:
    - HTTPException: If the organisation is not found (status_code=404) or if there is a server error (status_code=500).
    """
    repo = OrganisationRepository(session=db)
    service = OrganisationService(repo)
    if not await service.get_organisation_by_id(id):
        raise NotExistsIdException(id)
    else:

        return await service.get_organisation_by_id(id)

@app.delete("/organisation/delete/{id}")
async def delete_organisation(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Delete an organisation by its ID.

    Parameters:
    - id (int): The ID of the organisation to be deleted.
    - db (AsyncSession): The asynchronous database session.

    Returns:
    - dict: A dictionary with a success message if the organisation is deleted successfully.

    Raises:
    - HTTPException: If an error occurs during the deletion process.
    """
    repo = OrganisationRepository(session=db)
    service = OrganisationService(repo)
    if not await service.get_organisation_by_id(id):
        raise NotExistsIdException(id)
    else:
        return await service.delete_organisation(id)

#ADMIN
@app.post("/admin/add")
async def create_admin(admin: CreateAdmin, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new admin.

    Args:
        admin (CreateAdmin): The admin data to be created.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the admin is created successfully.

    Raises:
        HTTPException: If there is an error creating the admin.
    """
    try:
        repo = AdminRepository(session=db)
        new_admin = await repo.create_admin(admin)
        return {"message": "Admin created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admins")
async def get_admins(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all admins from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[Admin] - A list of admin objects retrieved from the database.

    Raises:
    - HTTPException: If there is an error retrieving the admins from the database.
    """
    try:
        repo = AdminRepository(session=db)
        admins = await repo.get_admins()
        return admins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/admin/{username}")
async def get_admin_by_name(username: str, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve an admin by their username.

    Args:
        username (str): The username of the admin to retrieve.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Admin: The admin object if found.

    Raises:
        HTTPException: If the admin is not found or an error occurs.
    """
    try:
        repo = AdminRepository(session=db)
        admin = await repo.get_admin_by_name(username)
        if admin:
            return admin
        else:
            raise HTTPException(status_code=404, detail="Admin not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/id/{id}")
async def get_admin_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve an admin by their ID.

    Args:
        id (int): The ID of the admin to retrieve.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Admin: The admin object if found.

    Raises:
        HTTPException: If the admin is not found or an error occurs.
    """
    try:
        repo = AdminRepository(session=db)
        admin = await repo.get_admin_by_id(id)
        if admin:
            return admin
        else:
            raise HTTPException(status_code=404, detail="Admin not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/delete/{id}")
async def delete_admin(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Delete an admin by their ID.

    Args:
        id (int): The ID of the admin to be deleted.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the admin is deleted successfully.

    Raises:
        HTTPException: If an error occurs during the deletion process.
    """
    try:
        repo = AdminRepository(session=db)
        admin = await repo.delete_admin_by_id(id)
        return {"message": "Admin deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#TEACHERS
@app.post("/teacher/add")
async def create_teacher(teacher: CreateTeacher, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = TeacherRepository(session=db)
        new_teacher = await repo.create_teacher(teacher)
        return {"message": "Teacher created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/teachers")
async def get_teachers(db: AsyncSession = Depends(get_async_db)):
    try:
        repo = TeacherRepository(session=db)
        teachers = await repo.get_teachers()
        return teachers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/teacher/id/{id}")
async def get_teacher_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = TeacherRepository(session=db)
        teacher = await repo.get_teacher_by_id(id)
        if teacher:
            return teacher
        else:
            raise HTTPException(status_code=404, detail="Teacher not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/teacher/{name}")
async def get_teacher_by_firstname(name: str, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = TeacherRepository(session=db)
        teacher = await repo.get_teacher_by_firstname(name)
        if teacher:
            return teacher
        else:
            raise HTTPException(status_code=404, detail="Teacher not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/teacher/delete/{id}")
async def delete_teacher(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = TeacherRepository(session=db)
        teacher = await repo.delete_teacher_by_id(id)
        return {"message": "Teacher deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/teacher/update/{id}")
async def update_teacher(id: int, teacher: UpdateTeacher, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = TeacherRepository(session=db)
        updated_teacher = await repo.update_teacher(id, teacher)
        if updated_teacher:
            return updated_teacher
        else:
            raise HTTPException(status_code=404, detail="Teacher not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#STUDENTS
@app.post("/student/add")
async def create_student(student: CreateStudent, db: AsyncSession = Depends(get_async_db)):
   repo = StudentRepository(session=db)
   service = StudentService(repo)
   existing_student_email = await service.get_student_by_email(student.email)
   if existing_student_email:
        raise StudentAlreadyExistsException(student.email)
   await service.create_student(student)
   return {"message": "Student created successfully"}

   

@app.get("/students")
async def get_students(db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    if not await service.get_students():
        raise NoStudentsFoundException()
    else:
      return await service.get_students()

    

@app.get("/student/id/{id}")
async def get_student_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    if not await service.get_student_by_id(id):
        raise StudentIdNotFoundException(id)
    else:
        return await service.get_student_by_id(id)
    

@app.get("/student/{name}")
async def get_student_by_firstname(name: str, db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    if not await service.get_student_by_firstname(name):
        raise StudentNotFoundException(name)
    else:
       return await service.get_student_by_firstname(name)

@app.delete("/student/delete/{id}")
async def delete_student(id: int, db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    if not await service.get_student_by_id(id):
        raise StudentIdNotFoundException(id)
    else:
        return await service.delete_student(id)


#COURSES

@app.post("/course/add")
async def create_course(course: CreateCourse, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new course.

    Args:
        course (CreateCourse): The course data to be created.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If an error occurs during the course creation process.
    """
    try:
        courseService = CourseService.from_async_repo(session=db)
        new_course = await courseService.create_course(course)
        return {"message": "Course created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses")
async def get_courses(db: AsyncSession = Depends(get_async_db)):
    try:
        courseService = CourseService.from_async_repo(session=db)
        courses = await courseService.get_courses()
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/course/{name}")
async def get_course_by_name(name: str, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = CourseRepository(session=db)
        course = await repo.get_course_by_name(name)
        if course:
            return course
        else:
            raise HTTPException(status_code=404, detail="Course not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/course/id/{id}")
async def get_course_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = CourseRepository(session=db)
        course = await repo.get_course_by_id(id)
        if course:
            return course
        else:
            raise HTTPException(status_code=404, detail="Course not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.delete("/course/delete/{id}")
async def delete_course(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = CourseRepository(session=db)
        course = await repo.delete_course_by_id(id)
        return {"message": "Course deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
        
@app.post("/assignment/add")
async def create_assignment(assignment: CreateAssignment, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new assignment.

    Args:
        assignment (CreateAssignment): The assignment data to be created.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        The newly created assignment.

    Raises:
        HTTPException: If there is an error creating the assignment.
    """
    try: 
        assignmentService = AssignmentService.from_async_repo(session=db)
        new_assignment = await assignmentService.create_assignment(assignment=assignment)
        return new_assignment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/assignments")
async def get_assignments(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all assignments from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[Assignment]: A list of assignments retrieved from the database.

    Raises:
    - HTTPException: If there is an error retrieving the assignments from the database.
    """
    try:
        assignmentService = AssignmentService.from_async_repo(session=db)
        assignments = await assignmentService.get_assignments()
        return assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/assignment/{assignment_id}")
async def get_assignment_by_id(assignment_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve an assignment by its ID.

    Args:
        assignment_id (int): The ID of the assignment to retrieve.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Assignment: The retrieved assignment.

    Raises:
        HTTPException: If the assignment is not found or an error occurs during retrieval.
    """
    try:
        assignmentService = AssignmentService.from_async_repo(session=db)
        assignment = await assignmentService.get_assignment_by_id(assignment_id)
        if assignment:
            return assignment
        else:
            raise HTTPException(status_code=404, detail="Assignment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/assignment/course/{course_id}")
async def get_assignments_by_course_id(course_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve assignments by course ID.

    Args:
        course_id (int): The ID of the course.

    Returns:
        List[Assignment]: A list of assignments associated with the given course ID.

    Raises:
        HTTPException: If there is an error retrieving the assignments.
    """
    try:
        assignmentService = AssignmentService.from_async_repo(session=db)
        assignments = await assignmentService.get_assignments_by_course_id(course_id)
        return assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/template/generate/{assignment_id}")
async def generate_template_solution(assignment_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Generate a template solution for a given assignment ID.

    Parameters:
    - assignment_id (int): The ID of the assignment for which to generate the template solution.
    - db (AsyncSession): The asynchronous database session.

    Returns:
    - template (str): The generated template solution.

    Raises:
    - HTTPException: If an error occurs during the generation of the template solution.
    """
    try:
        template_service = TemplateService.from_async_repo_and_open_ai_generator(session=db)
        template = await template_service.generate_template_solution(assignment_id=assignment_id)
        return template
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/templates")
async def get_all_templates(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all templates from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[Template] - A list of templates retrieved from the database.

    Raises:
    - HTTPException: If there is an error retrieving the templates.
    """
    try:
        repo = TemplateRepositoryAsync(session=db)
        templates = await repo.get_all_templates()
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/template/add")
async def add_template_solution(template_content: CreateTemplate, db: AsyncSession = Depends(get_async_db)):
    """
    Add a new template solution to the database.

    Args:
        template_content (CreateTemplate): The content of the template to be created.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary with a success message if the template is created successfully.

    Raises:
        HTTPException: If an error occurs during the template creation process.
    """
    try:
        repo = TemplateRepositoryAsync(session=db)
        new_template = await repo.create_template(template_content=template_content)
        return {"message": "Template created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/assignment/{assignment_id}/get_templates")
async def get_templates_for_assignment(assignment_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve templates for a specific assignment.

    Args:
        assignment_id (int): The ID of the assignment.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        List[Template]: A list of templates for the assignment.

    Raises:
        HTTPException: If there is an error retrieving the templates.
    """
    try:
        repo = TemplateRepositoryAsync(session=db)
        temples_for_assignment = await repo.get_templates_for_assignment(assignment_id)
        return temples_for_assignment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/student/assignment/submit")
async def student_submit_assignment(submission: CreateSubmission, db: AsyncSession = Depends(get_async_db)):
    """
    Submits a student assignment and returns the feedback.

    Args:
        submission (CreateSubmission): The submission object containing the assignment details and the content of the submission.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        Feedback: The feedback object generated for the submission by OpenAI's API.

    Raises:
        HTTPException: If an error occurs during the submission process.
    """
    try:
        submission_service = SubmissionService(session=db)
        feedback = await submission_service.student_submit_assignment(submission)
        return feedback
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/submissions")
async def get_all_submissions(db: AsyncSession = Depends(get_async_db)):
    try:
        repo = SubmissionRepository(session=db)
        submissions = await repo.get_all_submissions()
        return submissions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/submission/{submission_id}")
async def get_submission_by_id(submission_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = SubmissionRepository(session=db)
        submission = await repo.get_submission_by_id(submission_id)
        return submission
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/submission/feedback/{submission_id}")
async def get_feedback_by_submission_id(submission_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve feedback by submission ID.

    Args:
        submission_id (int): The ID of the submission.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        feedback: The feedback associated with the submission ID.

    Raises:
        HTTPException: If an error occurs while retrieving the feedback.
    """
    try:
        repo = FeedbackRepository(session=db)
        feedback = await repo.get_feedback_by_submission_id(submission_id)
        return feedback
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
#TABLE CREATION    
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def startup_event():
    await create_tables()
    await asyncio.sleep(5)  # Wait for tables to be created before starting the application

# Register the startup event
app.add_event_handler("startup", startup_event)

# Note: No need for the if __name__ == "__main__": block
