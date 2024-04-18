Organisation Endpoints
=======================


Overview
--------

An Organisation is an entity that represents an institution or a company. It is one of the top-level entities in the system. Organisations are created by Super Users of the system.

Attributes
----------

- **Name**: The name of the organisation.
- **Username**: The username of the organisation admin.
- **Password**: The password of the organisation admin.

Create Organisation Endpoint
----------------------------

.. autofunction:: app.main.create_organisation

.. code-block:: python

    """
    Create Organisation Example:
    ----------------------------
    To create a new organisation, send a POST request to `/organisation/add` with the necessary details in the request body.
    
    Example:
    ```
    curl -X POST "http://localhost:3000/organisation/add" \
    -H "Content-Type: application/json" \
    -d '{
      "name": "New Org",
      "username": "neworg123",
      "password": "securepassword"
    }'
    ```
    
    Upon successful creation, you'll receive a response similar to:
    ```json
    {
      "message": "Organisation created successfully"
    }
    ```
    """

Retrieve Organisations Endpoint
-------------------------------

.. autofunction:: app.main.get_organisations

Retrieve Organisation by Name Endpoint
--------------------------------------

.. autofunction:: app.main.get_organisation_by_name

Retrieve Organisation by ID Endpoint
------------------------------------

.. autofunction:: app.main.get_organisation_by_id

Delete Organisation Endpoint
-----------------------------

.. autofunction:: app.main.delete_organisation

Create Organisation Repository Function
----------------------------------------

.. automodule:: app.organisationRepo
    :members:
    :undoc-members:
    :show-inheritance:
