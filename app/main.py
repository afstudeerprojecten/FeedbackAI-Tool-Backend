from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.Auth.auth_service import AuthService
from app.Auth.auth_repository import AuthRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.Admin.Service.adminService import AdminService
from app.Assignment.Service.assignmentService import AssignmentService
from app.Course.Service.courseService import CourseService
from app.Feedback.Service.feedbackService import FeedbackService
from app.Templates.Service.templateService import TemplateService
from app.Submission.Service.submissionService import SubmissionService
from app.database import async_engine, SessionLocal as async_session
from app.Organisation.Repository.organisationRepo import OrganisationRepository
from app.Teacher.Repository.teacherRepo import TeacherRepository
from app.Student.Repository.studentRepo import StudentRepository
from app.Events.Repository.eventRepo import EventRepository
from app.EventsLog.Repository.eventLogRepo import EventLogRepository
from app.Organisation.Service.organisationService import OrganisationService
from app.Admin.Service.adminService import AdminService
from app.Student.Service.studentService import StudentService
from app.Teacher.Service.teacherService import TeacherService
from app.Events.Service.eventService import EventService
from app.EventsLog.Service.eventLogService import EventLogService
from app.exceptions import EntityAlreadyExistsException, EntityNotFoundException, EntityValidationException, entity_already_exists_handler, entity_not_found_handler, entity_validation_handler
from app.schemas import CreateTemplate, Organisation, CreateOrganisation, CreateAdmin, CreateTeacher, CreateCourse, CreateAssignment, UpdateTeacher, CreateSubmission, CreateStudent, CreateEvent, CreateEventLog, UserLogin, Token, EventLog
import asyncio
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}



app.add_exception_handler(EntityNotFoundException, entity_not_found_handler)
app.add_exception_handler(EntityAlreadyExistsException, entity_already_exists_handler)
app.add_exception_handler(EntityValidationException, entity_validation_handler)

# AUTHENTICATION
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_repo = AuthRepository()
auth_service = AuthService(auth_repo)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_db)):
    # Extract email from form_data.username
    email = form_data.username
    user, user_type = await auth_service.authenticate_user(db, email, form_data.password)
    access_token = auth_service.create_access_token(data={"sub": user.email, "user_type": user_type})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_async_db)):
    user, user_type = await auth_service.authenticate_user(db, user.email, user.password)
    access_token = auth_service.create_access_token(data={"sub": user.email, "user_type": user_type})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    auth_service.blacklist_token(token)
    return {"msg": "Successfully logged out"}

async def get_current_user_data(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
    user, user_type = await auth_service.get_current_user(token, db)
    return {"user": user, "user_type": user_type}

@app.get("/teachers-only")
async def read_teachers_only(user_data: dict = Depends(get_current_user_data)):
    user = user_data['user']
    user_type = user_data['user_type']
    if user_type != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Teachers only"
        )
    return {"message": f"Hello, {user.name}!"}


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
    return await service.create_organisation(organisation)
    
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
    adminService = AdminService.from_async_repo(session=db)
    return await adminService.create_admin(admin)
       
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
    adminService = AdminService.from_async_repo(session=db)
    return await adminService.get_admins()
    
        
    
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
    adminService = AdminService.from_async_repo(session=db)
    return await adminService.get_admin_by_username(username)
    

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
    adminService = AdminService.from_async_repo(session=db)
    return await adminService.get_admin_by_id(id)
    
  

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
    adminService = AdminService.from_async_repo(session=db)
    return await adminService.delete_admin_by_id(id)


#TEACHERS
@app.post("/teacher/add")
async def create_teacher(teacher: CreateTeacher, db: AsyncSession = Depends(get_async_db)):
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.create_teacher(teacher)



@app.get("/teachers")
async def get_teachers(db: AsyncSession = Depends(get_async_db)):
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.get_teachers()

@app.get("/teacher/id/{id}")
async def get_teacher_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.get_teacher_by_id(id)

@app.get("/teacher/{name}")
async def get_teacher_by_firstname(name: str, db: AsyncSession = Depends(get_async_db)):
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.get_teacher_by_firstname(name)

@app.delete("/teacher/delete/{id}")
async def delete_teacher(id: int, db: AsyncSession = Depends(get_async_db)):
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.delete_teacher(id)
    
@app.put("/teacher/update/{id}")
async def update_teacher(id: int, teacher: UpdateTeacher, db: AsyncSession = Depends(get_async_db)):
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.update_teacher(id, teacher)
    
#STUDENTS
@app.post("/student/add", status_code=status.HTTP_201_CREATED)
async def create_student(student: CreateStudent, db: AsyncSession = Depends(get_async_db)):
   repo = StudentRepository(session=db)
   service = StudentService(repo)
   return await service.create_student(student)

   

@app.get("/students")
async def get_students(db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    return await service.get_students()

    

@app.get("/student/id/{id}")
async def get_student_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    return await service.get_student_by_id(id)
    

@app.get("/student/{name}")
async def get_student_by_firstname(name: str, db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    return await service.get_student_by_firstname(name)

@app.delete("/student/delete/{id}")
async def delete_student(id: int, db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    return await service.delete_student(id)

@app.get("/student/name/{id}")
async def get_student_name_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    return await service.get_student_name_by_id(id)

@app.get("/student/email/{email}")
async def get_student_by_email(email: str, db: AsyncSession = Depends(get_async_db)):
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    return await service.get_student_by_email(email)

#EVENTS
@app.post("/event/add")
async def create_event(event: CreateEvent, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new event.

    Args:
        event (CreateEvent): The event data to be created.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the event is created successfully.

    Raises:
        HTTPException: If there is an error creating the event.
    """
    repo = EventRepository(session=db)
    eventService = EventService(repo)
    return await eventService.create_Event(event)

@app.get("/events")
async def get_events(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all events from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[Event] - A list of events retrieved from the database.

    Raises:
    - HTTPException: If there is an error retrieving the events from the database.
    """
    repo = EventRepository(session=db)
    eventService = EventService(repo)
    return await eventService.get_Events()

@app.get("/event/{event_id}")
async def get_event_by_id(event_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve an event by its ID.

    Args:
        event_id (int): The ID of the event to retrieve.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Event: The event object if found.

    Raises:
        HTTPException: If the event is not found or an error occurs.
    """
    repo = EventRepository(session=db)
    eventService = EventService(repo)
    return await eventService.get_Event_by_id(event_id)

@app.delete("/event/delete/{event_id}")
async def delete_event(event_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Delete an event by its ID.

    Args:
        event_id (int): The ID of the event to be deleted.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the event is deleted successfully.

    Raises:
        HTTPException: If an error occurs during the deletion process.
    """
    repo = EventRepository(session=db)
    eventService = EventService(repo)
    return await eventService.delete_Event(event_id)

@app.get("/event/name/{event_id}")
async def get_event_name_by_id(event_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve an event name by its ID.

    Args:
        event_id (int): The ID of the event to retrieve.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        str: The name of the event if found.

    Raises:
        HTTPException: If the event is not found or an error occurs.
    """
    repo = EventRepository(session=db)
    eventService = EventService(repo)
    return await eventService.get_Event_name_by_id(event_id)

#EVENTLOG
@app.post("/eventlog/add")
async def create_eventlog(eventlog: CreateEventLog, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new event log.

    Args:
        eventlog (CreateEventLog): The event log data to be created.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the event log is created successfully.

    Raises:
        HTTPException: If there is an error creating the event log.
    """
    repo = EventLogRepository(session=db)
    eventlogService = EventLogService(repo)
    return await eventlogService.create_EventLog(eventlog)

@app.post("/eventlog/add/test")
async def create_eventlog_for_testing(eventlog: EventLog, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new event log for testing purposes.

    Args:
        eventlog (CreateEventLog): The event log data to be created.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the event log is created successfully.

    Raises:
    - HTTPException: If there is an error creating the event log.
    """
    repo = EventLogRepository(session=db)
    eventlogService = EventLogService(repo)
    return await eventlogService.create_EventLog_for_testing(eventlog)

@app.get("/eventlogs")
async def get_eventlogs(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all event logs from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[EventLog] - A list of event logs retrieved from the database.

    Raises:
    - HTTPException: If there is an error retrieving the event logs from the database.
    """
    repo = EventLogRepository(session=db)
    eventlogService = EventLogService(repo)
    return await eventlogService.get_EventLogs()

@app.get("/eventlog/{eventlog_id}")
async def get_eventlog_by_id(eventlog_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve an event log by its ID.

    Args:
        eventlog_id (int): The ID of the event log to retrieve.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        EventLog: The event log object if found.

    Raises:
        HTTPException: If the event log is not found or an error occurs.
    """
    repo = EventLogRepository(session=db)
    eventlogService = EventLogService(repo)
    return await eventlogService.get_EventLog_by_id(eventlog_id)

@app.delete("/eventlog/delete/{eventlog_id}")
async def delete_eventlog(eventlog_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Delete an event log by its ID.

    Args:
        eventlog_id (int): The ID of the event log to be deleted.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the event log is deleted successfully.

    Raises:
        HTTPException: If an error occurs during the deletion process.
    """
    repo = EventLogRepository(session=db)
    eventlogService = EventLogService(repo)
    return await eventlogService.delete_EventLog(eventlog_id)

@app.get("/eventlog/event/{event_id}")
async def get_eventlog_by_event_id(event_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve event logs by event ID.

    Args:
        event_id (int): The ID of the event.

    Returns:
        List[EventLog]: A list of event logs associated with the given event ID.

    Raises:
        HTTPException: If there is an error retrieving the event logs.
    """
    repo = EventLogRepository(session=db)
    eventlogService = EventLogService(repo)
    return await eventlogService.get_EventLogs_by_event_id(event_id)

@app.get("/eventlog/user/{user_id}")
async def get_eventlog_by_user_id(user_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve event logs by user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[EventLog]: A list of event logs associated with the given user ID.

    Raises:
        HTTPException: If there is an error retrieving the event logs.
    """
    repo = EventLogRepository(session=db)
    eventlogService = EventLogService(repo)
    return await eventlogService.get_EventLog_by_user_id(user_id)

@app.put("/eventlog/update/{eventlog_id}")
async def update_eventlog(eventlog_id: int, eventlog: EventLog, db: AsyncSession = Depends(get_async_db)):
    """
    Update an event log by its ID.

    Args:
        eventlog_id (int): The ID of the event log to update.
        eventlog (EventLog): The updated event log data.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the event log is updated successfully.

    Raises:
        HTTPException: If an error occurs during the update process.
    """
    repo = EventLogRepository(session=db)
    eventlogService = EventLogService(repo)
    return await eventlogService.update_EventLog(eventlog_id, eventlog)

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
    courseService = CourseService.from_async_repo(session=db)
    new_course = await courseService.create_course(course)
    return {"message": "Course created successfully"}


@app.get("/courses")
async def get_courses(db: AsyncSession = Depends(get_async_db)):

    courseService = CourseService.from_async_repo(session=db)
    courses = await courseService.get_courses()
    return courses

    
@app.get("/course/{name}")
async def get_course_by_name(name: str, db: AsyncSession = Depends(get_async_db)):
    
    courseService = CourseService.from_async_repo(session=db)
    course = await courseService.get_course_by_name(name)
    return course


@app.get("/course/id/{id}")
async def get_course_by_id(id: int, db: AsyncSession = Depends(get_async_db)):

    courseService = CourseService.from_async_repo(session=db)
    course = await courseService.get_course_by_id(id)
    return course
    
    
@app.delete("/course/delete/{id}")
async def delete_course(id: int, db: AsyncSession = Depends(get_async_db)):
    
    courseService = CourseService.from_async_repo(session=db)
    course = await courseService.delete_course_by_id(id)
    return {"message": "Course deleted successfully"}

         
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
    assignmentService = AssignmentService.from_async_repo(session=db)
    new_assignment = await assignmentService.create_assignment(assignment=assignment)
    return new_assignment



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
    assignmentService = AssignmentService.from_async_repo(session=db)
    assignments = await assignmentService.get_assignments()
    return assignments

    
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
    assignmentService = AssignmentService.from_async_repo(session=db)
    assignment = await assignmentService.get_assignment_by_id(assignment_id)
    return assignment

    
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
    assignmentService = AssignmentService.from_async_repo(session=db)
    assignments = await assignmentService.get_assignments_by_course_id(course_id)
    return assignments


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
    template_service = TemplateService.from_async_repo_and_open_ai_generator(session=db)
    template = await template_service.generate_template_solution(assignment_id=assignment_id)
    return template
    

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
    template_service = TemplateService.from_async_repo_and_open_ai_generator(session=db)
    templates = await template_service.get_all_templates()
    return templates


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
    template_service = TemplateService.from_async_repo_and_open_ai_generator(session=db)
    new_template = await template_service.create_template(template=template_content)
    return {"message": "Template created successfully"}



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

    template_service = TemplateService.from_async_repo_and_open_ai_generator(session=db)
    temples_for_assignment = await template_service.get_templates_for_assignment(assignment_id)
    return temples_for_assignment


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
    submission_service = SubmissionService.from_async_repo_and_open_ai_feedback_generator(session=db)
    feedback = await submission_service.student_submit_assignment(submission)
    return feedback
    

@app.get("/submissions")
async def get_all_submissions(db: AsyncSession = Depends(get_async_db)):
    submission_service = SubmissionService.from_async_repo_and_open_ai_feedback_generator(session=db)
    submissions = await submission_service.get_all_submissions()
    return submissions


@app.get("/submission/{submission_id}")
async def get_submission_by_id(submission_id: int, db: AsyncSession = Depends(get_async_db)):
    
    submission_service = SubmissionService.from_async_repo_and_open_ai_feedback_generator(session=db)
    submission = await submission_service.get_submission_by_id(submission_id)
    return submission
    

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
    feedback_service = FeedbackService.from_async_repo(session=db)
    feedback = await feedback_service.get_feedback_by_submission_id(submission_id)
    return feedback
    
#TABLE CREATION    
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def startup_event():
    return
    # await create_tables()
    # await asyncio.sleep(0)  # Wait for tables to be created before starting the application

# Register the startup event
app.add_event_handler("startup", startup_event)

# Note: No need for the if __name__ == "__main__": block
