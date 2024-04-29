from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
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
from app.Feedback.Repository.feedbackRepoAsync import FeedbackRepositoryAsync
from app.Organisation.Service.organisationService import OrganisationService, AlreadyExistsException, NotExistsException, NotExistsIdException, NoOrganisationsFoundException
from app.Admin.Service.adminService import AdminService, AdminAlreadyExistsException, AdminNotFoundException, AdminIdNotFoundException, NoAdminsFoundException
from app.Student.Service.studentService import StudentService, StudentAlreadyExistsException, StudentNotFoundException, StudentIdNotFoundException, NoStudentsFoundException
from app.Teacher.Service.teacherService import TeacherService, TeacherAlreadyExistsException, TeacherNotFoundException, TeacherIdNotFoundException, NoTeachersFoundException
from app.exceptions import EntityNotFoundException, entity_not_found_exception
from app.schemas import CreateTemplate, Organisation, CreateOrganisation, CreateAdmin, CreateTeacher, CreateCourse, CreateAssignment, UpdateTeacher, CreateSubmission, CreateStudent
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
    """
    Root route returning a welcome message.

    Returns:
    - dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to the API, made with FastAPI!!"}


@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(request, exc):
    """
    Exception handler for AlreadyExistsException.

    Args:
    - request: The incoming request.
    - exc (AlreadyExistsException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 400.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Organisation with name '{exc.name}' already exists"},
    )

@app.exception_handler(NotExistsException)
async def not_exists_exception_handler(request, exc):
    """
    Exception handler for NotExistsException.

    Args:
    - request: The incoming request.
    - exc (NotExistsException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"Organisation with name '{exc.name}' does not exist"},
    )

@app.exception_handler(NotExistsIdException)
async def not_exists_id_exception_handler(request, exc):
    """
    Exception handler for NotExistsIdException.

    Args:
    - request: The incoming request.
    - exc (NotExistsIdException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"Organisation with ID '{exc.organisation_id}' does not exist"},
    )

@app.exception_handler(NoOrganisationsFoundException)
async def no_organisations_found_exception_handler(request, exc):
    """
    Exception handler for NoOrganisationsFoundException.

    Args:
    - request: The incoming request.
    - exc (NoOrganisationsFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": "No organisations found"},
    )

@app.exception_handler(StudentAlreadyExistsException)
async def student_already_exists_exception_handler(request, exc):
    """
    Exception handler for StudentAlreadyExistsException.

    Args:
    - request: The incoming request.
    - exc (StudentAlreadyExistsException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 400.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Student with email '{exc.name}' already exists"},
    )

@app.exception_handler(StudentNotFoundException)
async def student_not_found_exception_handler(request, exc):
    """
    Exception handler for StudentNotFoundException.

    Args:
    - request: The incoming request.
    - exc (StudentNotFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"Student with name '{exc.name}' does not exist"},
    )

@app.exception_handler(StudentIdNotFoundException)
async def student_id_not_found_exception_handler(request, exc):
    """
    Exception handler for StudentIdNotFoundException.

    Args:
    - request: The incoming request.
    - exc (StudentIdNotFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"Student with ID '{exc.student_id}' does not exist"},
    )

@app.exception_handler(NoStudentsFoundException)
async def no_students_found_exception_handler(request, exc):
    """
    Exception handler for NoStudentsFoundException.

    Args:
    - request: The incoming request.
    - exc (NoStudentsFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": "No students found"},
    )

@app.exception_handler(TeacherAlreadyExistsException)
async def teacher_already_exists_exception_handler(request, exc):
    """
    Exception handler for TeacherAlreadyExistsException.

    Args:
    - request: The incoming request.
    - exc (TeacherAlreadyExistsException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 400.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Teacher with email '{exc.name}' already exists"},
    )

@app.exception_handler(TeacherNotFoundException)
async def teacher_not_found_exception_handler(request, exc):
    """
    Exception handler for TeacherNotFoundException.

    Args:
    - request: The incoming request.
    - exc (TeacherNotFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"Teacher with name '{exc.name}' does not exist"},
    )

@app.exception_handler(TeacherIdNotFoundException)
async def teacher_id_not_found_exception_handler(request, exc):
    """
    Exception handler for TeacherIdNotFoundException.

    Args:
    - request: The incoming request.
    - exc (TeacherIdNotFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"Teacher with ID '{exc.teacher_id}' does not exist"},
    )

@app.exception_handler(NoTeachersFoundException)
async def no_teachers_found_exception_handler(request, exc):
    """
    Exception handler for NoTeachersFoundException.

    Args:
    - request: The incoming request.
    - exc (NoTeachersFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": "No teachers found"},
    )

@app.exception_handler(AdminAlreadyExistsException)
async def admin_already_exists_exception_handler(request, exc):
    """
    Exception handler for AdminAlreadyExistsException.

    Args:
    - request: The incoming request.
    - exc (AdminAlreadyExistsException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 400.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Admin with username '{exc.username}' already exists"},
    )

@app.exception_handler(AdminNotFoundException)
async def admin_not_found_exception_handler(request, exc):
    """
    Exception handler for AdminNotFoundException.

    Args:
    - request: The incoming request.
    - exc (AdminNotFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"Admin with username '{exc.username}' does not exist"},
    )

@app.exception_handler(AdminIdNotFoundException)
async def admin_id_not_found_exception_handler(request, exc):
    """
    Exception handler for AdminIdNotFoundException.

    Args:
    - request: The incoming request.
    - exc (AdminIdNotFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": f"Admin with ID '{exc.admin_id}' does not exist"},
    )

@app.exception_handler(NoAdminsFoundException)
async def no_admins_found_exception_handler(request, exc):
    """
    Exception handler for NoAdminsFoundException.

    Args:
    - request: The incoming request.
    - exc (NoAdminsFoundException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 404.
    """
    return JSONResponse(
        status_code=404,
        content={"message": "No admins found"},
    )

@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(request, exc):
    """
    Exception handler for AlreadyExistsException.

    Args:
    - request: The incoming request.
    - exc (AlreadyExistsException): The exception instance.

    Returns:
    - JSONResponse: JSON response with error message and status code 400.
    """
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
        AlreadyExistsException: If an organisation with the same name already exists.
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
    - NoOrganisationsFoundException: If no organisations are found in the database.
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
        NotExistsException: If the organisation with the specified name does not exist.
        HTTPException: If an error occurs.
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
    - NotExistsIdException: If the organisation with the specified ID does not exist.
    - HTTPException: If there is an error retrieving the organisation.
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
    - NotExistsIdException: If the organisation with the specified ID does not exist.
    - HTTPException: If there is an error deleting the organisation.
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
        AdminAlreadyExistsException: If an admin with the same username already exists.
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
    - NoAdminsFoundException: If no admins are found in the database.
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
        AdminNotFoundException: If the admin with the specified username does not exist.
        HTTPException: If an error occurs.
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
        AdminIdNotFoundException: If the admin with the specified ID does not exist.
        HTTPException: If there is an error retrieving the admin.
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
        AdminIdNotFoundException: If the admin with the specified ID does not exist.
        HTTPException: If there is an error deleting the admin.
    """
    adminService = AdminService.from_async_repo(session=db)
    return await adminService.delete_admin_by_id(id)


#TEACHERS
@app.post("/teacher/add")
async def create_teacher(teacher: CreateTeacher, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new teacher.

    Args:
        teacher (CreateTeacher): The teacher data to be created.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the teacher is created successfully.

    Raises:
        TeacherAlreadyExistsException: If a teacher with the same email already exists.
        HTTPException: If there is an error creating the teacher.
    """
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.create_teacher(teacher)



@app.get("/teachers")
async def get_teachers(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all teachers from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[Teacher] - A list of teacher objects retrieved from the database.

    Raises:
    - NoTeachersFoundException: If no teachers are found in the database.
    - HTTPException: If there is an error retrieving the teachers from the database.
    """
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.get_teachers()

@app.get("/teacher/id/{id}")
async def get_teacher_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a teacher by their ID.

    Args:
        id (int): The ID of the teacher to retrieve.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Teacher: The teacher object if found.

    Raises:
        TeacherIdNotFoundException: If the teacher with the specified ID does not exist.
        HTTPException: If there is an error retrieving the teacher.
    """
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.get_teacher_by_id(id)

@app.get("/teacher/{name}")
async def get_teacher_by_firstname(name: str, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a teacher by their first name.

    Args:
        name (str): The first name of the teacher.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Teacher: The teacher object if found.

    Raises:
        TeacherNotFoundException: If the teacher with the specified name does not exist.
        HTTPException: If there is an error retrieving the teacher.
    """
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.get_teacher_by_firstname(name)

@app.delete("/teacher/delete/{id}")
async def delete_teacher(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Delete a teacher by their ID.

    Args:
        id (int): The ID of the teacher to be deleted.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the teacher is deleted successfully.

    Raises:
        TeacherIdNotFoundException: If the teacher with the specified ID does not exist.
        HTTPException: If there is an error deleting the teacher.
    """
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.delete_teacher(id)
    
@app.put("/teacher/update/{id}")
async def update_teacher(id: int, teacher: UpdateTeacher, db: AsyncSession = Depends(get_async_db)):
    """
    Update a teacher.

    Args:
        id (int): The ID of the teacher to update.
        teacher (UpdateTeacher): The updated teacher data.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the teacher is updated successfully.

    Raises:
        TeacherIdNotFoundException: If the teacher with the specified ID does not exist.
        HTTPException: If there is an error updating the teacher.
    """
    repo = TeacherRepository(session=db)
    service = TeacherService(repo)
    return await service.update_teacher(id, teacher)
    
#STUDENTS
@app.post("/student/add", status_code=status.HTTP_201_CREATED)
async def create_student(student: CreateStudent, db: AsyncSession = Depends(get_async_db)):
   """
    Create a new student.

    Args:
        student (CreateStudent): The student data to be created.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the student is created successfully.

    Raises:
        StudentAlreadyExistsException: If a student with the same email already exists.
        HTTPException: If there is an error creating the student.
   """
   repo = StudentRepository(session=db)
   service = StudentService(repo)
   return await service.create_student(student)

   

@app.get("/students")
async def get_students(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all students from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[Student] - A list of student objects retrieved from the database.

    Raises:
    - NoStudentsFoundException: If no students are found in the database.
    - HTTPException: If there is an error retrieving the students from the database.
    """
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    return await service.get_students()

    

@app.get("/student/id/{id}")
async def get_student_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a student by their ID.

    Args:
        id (int): The ID of the student to retrieve.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Student: The student object if found.

    Raises:
        StudentIdNotFoundException: If the student with the specified ID does not exist.
        HTTPException: If there is an error retrieving the student.
    """
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    return await service.get_student_by_id(id)
    

@app.get("/student/{name}")
async def get_student_by_firstname(name: str, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a student by their first name.

    Args:
        name (str): The first name of the student.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Student: The student object if found.

    Raises:
        StudentNotFoundException: If the student with the specified name does not exist.
        HTTPException: If there is an error retrieving the student.
    """
    repo = StudentRepository(session=db)
    service = StudentService(repo)
    return await service.get_student_by_firstname(name)

@app.delete("/student/delete/{id}")
async def delete_student(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Delete a student by their ID.

    Args:
        id (int): The ID of the student to be deleted.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the student is deleted successfully.

    Raises:
        StudentIdNotFoundException: If the student with the specified ID does not exist.
        HTTPException: If there is an error deleting the student.
    """
    repo = StudentRepository(session=db)
    service = StudentService(repo)
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
        CourseAlreadyExistsException: If a course with the same name already exists.
        HTTPException: If an error occurs during the course creation process.
    """
    courseService = CourseService.from_async_repo(session=db)
    new_course = await courseService.create_course(course)
    return {"message": "Course created successfully"}


@app.get("/courses")
async def get_courses(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all courses from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[Course] - A list of course objects retrieved from the database.

    Raises:
    - NoCoursesFoundException: If no courses are found in the database.
    - HTTPException: If there is an error retrieving the courses from the database.
    """
    courseService = CourseService.from_async_repo(session=db)
    courses = await courseService.get_courses()
    return courses

    
@app.get("/course/{name}")
async def get_course_by_name(name: str, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a course by its name.

    Args:
        name (str): The name of the course.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Course: The course object if found.

    Raises:
        CourseNotFoundException: If the course with the specified name does not exist.
        HTTPException: If there is an error retrieving the course.
    """
    courseService = CourseService.from_async_repo(session=db)
    course = await courseService.get_course_by_name(name)
    return course


@app.get("/course/id/{id}")
async def get_course_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a course by its ID.

    Args:
        id (int): The ID of the course.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Course: The course object if found.

    Raises:
        CourseIdNotFoundException: If the course with the specified ID does not exist.
        HTTPException: If there is an error retrieving the course.
    """
    courseService = CourseService.from_async_repo(session=db)
    course = await courseService.get_course_by_id(id)
    return course
    
    
@app.delete("/course/delete/{id}")
async def delete_course(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Delete a course by its ID.

    Args:
        id (int): The ID of the course to be deleted.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the course is deleted successfully.

    Raises:
        CourseIdNotFoundException: If the course with the specified ID does not exist.
        HTTPException: If there is an error deleting the course.
    """
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
        Assignment: The newly created assignment.

    Raises:
        UniqueAssignmentTitlePerCourseException: If an assignment with the same title already exists for the course.
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
    - NoAssignmentsFoundException: If no assignments are found in the database.
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
        EntityNotFoundException: If the assignment with the specified ID does not exist.
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

    Args:
        assignment_id (int): The ID of the assignment for which to generate the template solution.
        db (AsyncSession): The asynchronous database session.

    Returns:
        str: The generated template solution.

    Raises:
        EntityNotFoundException: If the assignment with the specified ID does not exist.
        HTTPException: If an error occurs during the generation of the template solution.
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
    - EntityNotFoundException: If there is an error retrieving the templates.
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
        EntityNotFoundException: If the assignment with the specified ID does not exist.
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
        EntityNotFoundException: If the assignment with the specified ID does not exist.
        HTTPException: If an error occurs during the submission process.
    """
    submission_service = SubmissionService.from_async_repo_and_open_ai_feedback_generator(session=db)
    feedback = await submission_service.student_submit_assignment(submission)
    return feedback
    

@app.get("/submissions")
async def get_all_submissions(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all submissions from the database.

    Parameters:
    - db: AsyncSession - The async database session.

    Returns:
    - List[Submission]: A list of submissions retrieved from the database.

    Raises:
    - HTTPException: If there is an error retrieving the submissions.
    """
    submission_service = SubmissionService.from_async_repo_and_open_ai_feedback_generator(session=db)
    submissions = await submission_service.get_all_submissions()
    return submissions


@app.get("/submission/{submission_id}")
async def get_submission_by_id(submission_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a submission by its ID.

    Args:
        submission_id (int): The ID of the submission.
        db (AsyncSession, optional): The async database session. Defaults to Depends(get_async_db).

    Returns:
        Submission: The submission object.

    Raises:
        EntityNotFoundException: If the submission with the specified ID does not exist.
        HTTPException: If there is an error retrieving the submission.
    """
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
        Feedback: The feedback associated with the submission ID.

    Raises:
        EntityNotFoundException: If the feedback with the specified ID does not exist.
        HTTPException: If there is an error retrieving the feedback.
    """
    feedback_service = FeedbackService.from_async_repo(session=db)
    feedback = await feedback_service.get_feedback_by_submission_id(submission_id)
    return feedback


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
