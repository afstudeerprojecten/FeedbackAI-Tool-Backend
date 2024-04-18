from fastapi import FastAPI, HTTPException, Depends, FastAPI, UploadFile, Form, File
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from app.documentService import DocumentService
from app.submissionRepo import SubmissionRepository
from app.submissionService import SubmissionService
from app.templateRepo import TemplateRepository
from app.templateService import TemplateService
from app.database import async_engine, SessionLocal as async_session
from app.organisationRepo import OrganisationRepository
from app.adminRepo import AdminRepository
from app.courseRepo import CourseRepository
from app.teacherRepo import TeacherRepository
from app.studentRepo import StudentRepository
from app.feedbackRepo import FeedbackRepository
from app.schemas import CreateTemplate, Organisation, CreateOrganisation, CreateAdmin, CreateTeacher, CreateCourse, CreateAssignment, UpdateTeacher, CreateSubmission, CreateStudent
import asyncio
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware
from app.assignmentRepo import AssignmentRepository
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


# ORGANISATION
@app.post("/organisation/add")
async def create_organisation(organisation: CreateOrganisation, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = OrganisationRepository(session=db)  # Pass the session directly to the OrganisationRepository
        new_organisation = await repo.create_organisation(organisation)  # Create the new organisation
        return {"message": "Organisation created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/organisations")
async def get_organisations(db: AsyncSession = Depends(get_async_db)):
    try:
        repo = OrganisationRepository(session=db)
        organisations = await repo.get_organisations()
        return organisations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/organisation/{name}")
async def get_organisation_by_name(name: str, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = OrganisationRepository(session=db)
        organisation = await repo.get_organisation_by_name(name)
        if organisation:
            return organisation
        else:
            raise HTTPException(status_code=404, detail="Organisation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/organisation/id/{id}")
async def get_organisation_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = OrganisationRepository(session=db)
        organisation = await repo.get_organisation_by_id(id)
        if organisation:
            return organisation
        else:
            raise HTTPException(status_code=404, detail="Organisation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/organisation/delete/{id}")
async def delete_organisation(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = OrganisationRepository(session=db)
        organisation = await repo.delete_organisation(id)
        return {"message": "Organisation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#ADMIN
@app.post("/admin/add")
async def create_admin(admin: CreateAdmin, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = AdminRepository(session=db)
        new_admin = await repo.create_admin(admin)
        return {"message": "Admin created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admins")
async def get_admins(db: AsyncSession = Depends(get_async_db)):
    try:
        repo = AdminRepository(session=db)
        admins = await repo.get_admins()
        return admins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/admin/{username}")
async def get_admin_by_name(username: str, db: AsyncSession = Depends(get_async_db)):
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
    try:
        repo = StudentRepository(session=db)
        new_student = await repo.create_student(student)
        return {"message": "Student created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students")
async def get_students(db: AsyncSession = Depends(get_async_db)):
    try:
        repo = StudentRepository(session=db)
        students = await repo.get_students()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/student/id/{id}")
async def get_student_by_id(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = StudentRepository(session=db)
        student = await repo.get_student_by_id(id)
        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/student/{name}")
async def get_student_by_firstname(name: str, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = StudentRepository(session=db)
        student = await repo.get_student_by_firstname(name)
        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/student/delete/{id}")
async def delete_student(id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = StudentRepository(session=db)
        student = await repo.delete_student_by_id(id)
        return {"message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#COURSES
@app.post("/course/add")
async def create_course(course: CreateCourse, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = CourseRepository(session=db)
        new_course = await repo.create_course(course)
        return {"message": "Course created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses")
async def get_courses(db: AsyncSession = Depends(get_async_db)):
    try:
        repo = CourseRepository(session=db)
        courses = await repo.get_courses()
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
    try: 
        repo = AssignmentRepository(session=db)
        new_assignment = await repo.create_assignment(assignment)
        return new_assignment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/assignments")
async def get_assignments(db: AsyncSession = Depends(get_async_db)):
    try:
        repo = AssignmentRepository(session=db) 
        assignments = await repo.get_assignments()
        return assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/assignment/{assignment_id}")
async def get_assignment_by_id(assignment_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = AssignmentRepository(session=db)
        assignment = await repo.get_assignment_by_id(assignment_id)
        if assignment:
            return assignment
        else:
            raise HTTPException(status_code=404, detail="Assignment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/assignment/course/{course_id}")
async def get_assignments_by_course_id(course_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = AssignmentRepository(session=db)
        assignments = await repo.get_assignments_by_course_id(course_id)
        return assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/template/generate/{assignment_id}")
async def generate_template_solution(assignment_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        template_service = TemplateService(session=db)
        template = await template_service.generate_template_solution(assignment_id=assignment_id)
        return template
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/templates")
async def get_all_templates(db: AsyncSession = Depends(get_async_db)):
    try:
        repo = TemplateRepository(session=db)
        templates = await repo.get_all_templates()
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/template/add")
async def add_template_solution(template_content: CreateTemplate, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = TemplateRepository(session=db)
        new_template = await repo.create_template(template_content=template_content)
        return {"message": "Template created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/assignment/{assignment_id}/get_templates")
async def get_templates_for_assignment(assignment_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = TemplateRepository(session=db)
        temples_for_assignment = await repo.get_templates_for_assignment(assignment_id)
        return temples_for_assignment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/student/assignment/submit")
async def student_submit_assignment(submission: CreateSubmission, db: AsyncSession = Depends(get_async_db)):
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
    try:
        repo = FeedbackRepository(session=db)
        feedback = await repo.get_feedback_by_submission_id(submission_id)
        return feedback
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/courses/teacher/{teacher_id}")
async def get_all_courses_from_teacher_by_teacher_id(teacher_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        repo = CourseRepository(session=db)
        courses = await repo.get_courses_by_teacher_id(teacher_id)
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/courses/teacher/upload/document")
async def teacher_uploads_documents_to_course(
    teacher_id: int = Form(...),
    course_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db)):
    try:
        
        documentService = DocumentService(session=db)

        output = await documentService.uploadDocument(teacher_id, course_id, file)

        return output

    except Exception as e:
        print(e)
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
