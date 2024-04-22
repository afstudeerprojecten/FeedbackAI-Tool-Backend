Assignment Endpoints
====================

Generate Template Solution Endpoint
------------------------------------

This endpoint generates a template solution for a given assignment ID.

.. autofunction:: app.main.generate_template_solution

Generate Template Solution Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The process of generating a template solution involves the following steps:

1. **Retrieve Assignment Details**:
   - The assignment details, including the assignment title and description, are retrieved from the database.

2. **Prepare Conversation Messages**:
   - A conversation between a teacher and an assistant teacher is simulated using an AI model.
   - The teacher provides instructions for the assignment, and the assistant teacher generates a solution.
   - Feedback is provided by the teacher, and the assistant teacher generates another solution based on the feedback, and so on.

3. **Generate Template Solution**:
   - The generated template solution is returned as a response.

Generate Template Solution Service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: app.templateService.TemplateService.generate_template_solution

Example
~~~~~~~

To generate a template solution for a specific assignment, send a GET request to `/template/generate/{assignment_id}` where `{assignment_id}` is the ID of the assignment.

.. code-block:: http

    GET /template/generate/123 HTTP/1.1
    Host: example.com

Response
~~~~~~~~

Upon successful generation, you'll receive a response containing the generated template solution.

.. _generate_template_solution_example:

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "template_solution": "Generated template solution content..."
    }





