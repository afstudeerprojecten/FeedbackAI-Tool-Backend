from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI, HTTPException, Depends, status, FastAPI, UploadFile, Form, File
import aiofiles
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.Document.Service.documentService import DocumentService
from app.Admin.Service.adminService import AdminService
from app.Assignment.Service.assignmentService import AssignmentService, UniqueAssignmentTitlePerCourseException, unique_assignment_title_per_course_id_combination_exception_handler
from app.Course.Service.courseService import CourseService, UniqueCourseNameAndTeacherIdCombinationExcepton, unique_course_name_and_teacher_id_combination_exception_handler
from app.Feedback.Service.feedbackService import FeedbackService
from app.Templates.Service.templateService import TemplateService
from app.Submission.Repository.submissionRepoAsync import SubmissionRepositoryAsync
from app.Submission.Service.submissionService import SubmissionService
from app.Templates.Repository.templateRepoAsync import TemplateRepositoryAsync
from app.database import async_engine, SessionLocal as async_session
from app.Organisation.Repository.organisationRepo import OrganisationRepository
from app.Admin.Repository.adminRepoAsync import AdminRepositoryAsync
from app.Course.Repository.courseRepoAsync import CourseRepositoryAsync
from app.Teacher.Repository.teacherRepo import TeacherRepository
from app.Student.Repository.studentRepo import StudentRepository
from app.Events.Repository.eventRepo import EventRepository
from app.EventsLog.Repository.eventLogRepo import EventLogRepository
from app.Feedback.Repository.feedbackRepoAsync import FeedbackRepositoryAsync
from app.Organisation.Service.organisationService import OrganisationService, AlreadyExistsException, NotExistsException, NotExistsIdException, NoOrganisationsFoundException
from app.Admin.Service.adminService import AdminService, AdminAlreadyExistsException, AdminNotFoundException, AdminIdNotFoundException, NoAdminsFoundException
from app.Student.Service.studentService import StudentService, StudentAlreadyExistsException, StudentNotFoundException, StudentIdNotFoundException, NoStudentsFoundException
from app.Teacher.Service.teacherService import TeacherService, TeacherAlreadyExistsException, TeacherNotFoundException, TeacherIdNotFoundException, NoTeachersFoundException
from app.Events.Service.eventService import EventService, EventAlreadyExistsException, EventNotFoundException, EventIdNotFoundException, NoEventsFoundException
from app.EventsLog.Service.eventLogService import EventLogService, EventLogAlreadyExistsException, EventLogNotFoundException, EventLogIdNotFoundException, NoEventLogsFoundException, UserNotFoundException, EventNotFoundException
from app.exceptions import EntityNotFoundException, entity_not_found_exception
from app.schemas import CreateTemplate, Organisation, CreateOrganisation, CreateAdmin, CreateTeacher, CreateCourse, CreateAssignment, UpdateTeacher, CreateSubmission, CreateStudent, CreateEvent, CreateEventLog
import asyncio
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware
import os
from app.vector_database import create_persistent_vector_db_folder
from app.vector_database import reset_vector_db



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
        content={"message": f"Student with email '{exc.name}' already exists"},
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

@app.exception_handler(TeacherAlreadyExistsException)
async def teacher_already_exists_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": f"Teacher with email '{exc.name}' already exists"},
    )

@app.exception_handler(TeacherNotFoundException)
async def teacher_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Teacher with name '{exc.name}' does not exist"},
    )

@app.exception_handler(TeacherIdNotFoundException)
async def teacher_id_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Teacher with ID '{exc.teacher_id}' does not exist"},
    )

@app.exception_handler(NoTeachersFoundException)
async def no_teachers_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "No teachers found"},
    )

@app.exception_handler(EventAlreadyExistsException)
async def event_already_exists_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": f"Event with ID '{exc.event_id}' already exists"},
    )

@app.exception_handler(EventNotFoundException)
async def event_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Event with ID '{exc.event_id}' does not exist"},
    )

@app.exception_handler(NoEventsFoundException)
async def no_events_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "No events found"},
    )

@app.exception_handler(EventLogAlreadyExistsException)
async def event_log_already_exists_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": f"EventLog with ID '{exc.eventlog_id}' already exists"},
    )

@app.exception_handler(EventLogNotFoundException)
async def event_log_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"EventLog with ID '{exc.eventlog_id}' does not exist"},
    )

@app.exception_handler(EventLogIdNotFoundException)
async def event_log_id_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"EventLog with ID '{exc.eventlog_id}' does not exist"},
    )

@app.exception_handler(NoEventLogsFoundException)
async def no_event_logs_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "No event logs found"},
    )

@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"User with ID '{exc.id}' does not exist"},
    )

@app.exception_handler(EventNotFoundException)
async def event_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Event with ID '{exc.id}' does not exist"},
    )

@app.exception_handler(AdminAlreadyExistsException)
async def admin_already_exists_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": f"Admin with username '{exc.username}' already exists"},
    )

@app.exception_handler(AdminNotFoundException)
async def admin_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Admin with username '{exc.username}' does not exist"},
    )

@app.exception_handler(AdminIdNotFoundException)
async def admin_id_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Admin with ID '{exc.admin_id}' does not exist"},
    )

@app.exception_handler(NoAdminsFoundException)
async def no_admins_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "No admins found"},
    )

@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": f"Organisation with name '{exc.name}' already exists"},
    )




app.add_exception_handler(UniqueCourseNameAndTeacherIdCombinationExcepton, unique_course_name_and_teacher_id_combination_exception_handler)
app.add_exception_handler(EntityNotFoundException, entity_not_found_exception)
app.add_exception_handler(UniqueAssignmentTitlePerCourseException, unique_assignment_title_per_course_id_combination_exception_handler)

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
    return await eventlogService.get_EventLog_by_event_id(event_id)

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

@app.get("/courses/teacher/{teacher_id}")
async def get_all_courses_from_teacher_by_teacher_id(teacher_id: int, db: AsyncSession = Depends(get_async_db)):
    try:

        # maak hier service call van
        # en moet aanpassen in courserepo interface nog
        repo = CourseRepositoryAsync(session=db)
        courses = await repo.get_courses_by_teacher_id(teacher_id)
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Maak hier put van
@app.post("/courses/teacher/upload/document")
async def teacher_uploads_documents_to_course(
    teacher_id: int = Form(...),
    course_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db)):
    try:
        documentService = DocumentService.from_async_repos_and_local_files_and_nomic_embed_and_chroma(session=db)

        output = await documentService.uploadDocument(teacher_id, course_id, file)

        return output

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.delete('/vectordatabase/reset')
async def vector_database_reset():
    try:
        await reset_vector_db()
        return {"message": "Vector Database succesfully reset"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    
#TABLE CREATION    
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def startup_event():
    await create_tables()
    await create_persistent_vector_db_folder()
    await asyncio.sleep(5)  # Wait for tables to be created before starting the application

# Register the startup event
app.add_event_handler("startup", startup_event)

# Note: No need for the if __name__ == "__main__": block
