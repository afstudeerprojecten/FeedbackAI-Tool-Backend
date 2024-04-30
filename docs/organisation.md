# Organisation API References

The `Organisation` object represents an educational institution such as a school, college, or university. It serves as the central entity that manages teachers, courses, and students within the educational system.

## Organisation Attributes

An `Organisation` object typically includes attributes such as:

- **ID**: A unique identifier for the organisation within the system.
- **Name**: The name of the organisation.
- **Username**: The username used by the organisation to log in.
- **Password**: The password used by the organisation to log in.

### Relationship to Teachers

Teachers have an Organisation ID Attribute that links them to the organisation they are affiliated with. This relationship signifies the organisation to which the teacher belongs.

### Relationship to Students

Students have an Organisation ID Attribute that links them to the organisation they are affiliated with. This relationship signifies the organisation to which the student belongs.

## API Endpoints

::: app.main.create_organisation

::: app.main.get_organisations

::: app.main.get_organisation_by_id

::: app.main.get_organisation_by_name

::: app.main.delete_organisation

