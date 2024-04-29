import pytest
from unittest.mock import AsyncMock, MagicMock
from app.models import Course
from app.schemas import CreateCourse
from app.Course.Service.courseService import CourseService, UniqueCourseNameAndTeacherIdCombinationExcepton, EntityNotFoundException

@pytest.fixture
def course_service():
    course_repository_mock = AsyncMock()
    return CourseService(courseRepository=course_repository_mock)

@pytest.mark.asyncio
async def test_create_course(course_service):
    course_service.courseRepository.get_course_by_name_and_teacher_id.return_value = None

    # Mock the repository's create_course method to return a course
    course_service.courseRepository.create_course.return_value = Course(id=1, name="Test Course", teacher_id=1)

    # Call the create_course method
    created_course = await course_service.create_course(CreateCourse(name="Test Course", teacher_id=1))

    # Check if the course is created
    assert created_course.name == "Test Course"
    assert created_course.teacher_id == 1

@pytest.mark.asyncio
async def test_get_courses(course_service):
    course_service.courseRepository.get_courses.return_value = [
        Course(id=1, name="Course 1", teacher_id=1),
        Course(id=2, name="Course 2", teacher_id=2)
    ]

    # Call the get_courses method
    courses = await course_service.get_courses()

    # Check if the courses are returned
    assert len(courses) == 2
    assert courses[0].name == "Course 1"
    assert courses[1].name == "Course 2"

@pytest.mark.asyncio
async def test_get_course_by_name(course_service):
    course_service.courseRepository.get_course_by_name.return_value = Course(id=1, name="Test Course", teacher_id=1)

    # Call the get_course_by_name method
    course = await course_service.get_course_by_name("Test Course")

    # Check if the course is returned
    assert course.name == "Test Course"

@pytest.mark.asyncio
async def test_get_course_by_name_not_found(course_service):
    course_service.courseRepository.get_course_by_name.return_value = None

    # Call the get_course_by_name method
    with pytest.raises(EntityNotFoundException):
        await course_service.get_course_by_name("Non-existent Course")

@pytest.mark.asyncio
async def test_get_course_by_id(course_service):
    course_service.courseRepository.get_course_by_id.return_value = Course(id=1, name="Test Course", teacher_id=1)

    # Call the get_course_by_id method
    course = await course_service.get_course_by_id(1)

    # Check if the course is returned
    assert course.name == "Test Course"

@pytest.mark.asyncio
async def test_get_course_by_id_not_found(course_service):
    course_service.courseRepository.get_course_by_id.return_value = None

    # Call the get_course_by_id method
    with pytest.raises(EntityNotFoundException):
        await course_service.get_course_by_id(999)


@pytest.mark.asyncio
async def test_delete_course_by_id(course_service):
    course_service.courseRepository.delete_course_by_id.return_value = Course(id=1,name="Test Course", teacher_id=1)
    
    # call the delete_course_by_id method
    await course_service.delete_course_by_id(1)