# Teacher API References

## Teacher Object and its Relationship to Organisation and Courses

The `Teacher` object represents an educator or instructor within the educational system. In many educational institutions, teachers play a crucial role in delivering curriculum content, facilitating learning activities, and assessing student progress.

## Teacher Attributes

A `Teacher` object typically includes attributes such as:

- **ID**: A unique identifier for the teacher within the system.
- **Name**: The name of the teacher.
- **First Name**: The first name of the teacher.
- **Email**: Contact information for the teacher.
- **Organisation**: The educational institution or organisation to which the teacher is affiliated.

### Relationship to Organisation

In the context of an educational system, a `Teacher` is often associated with an `Organisation`, such as a school, college, or university.

### Relationship to Courses

Teachers are typically responsible for teaching one or more courses within an educational institution. A course can only be taught by one teacher.

## API Endpoints

::: app.main.create_teacher

::: app.main.get_teachers

::: app.main.get_teacher_by_id

::: app.main.get_teacher_by_firstname

::: app.main.update_teacher

::: app.main.delete_teacher
