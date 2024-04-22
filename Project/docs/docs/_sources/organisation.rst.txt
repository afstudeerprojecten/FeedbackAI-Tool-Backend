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

This endpoint creates a new organisation in the database.

.. autofunction:: app.main.create_organisation

Example
~~~~~~~

To create a new organisation, send a POST request to `/organisation/add` with the necessary details in the request body.

.. code-block:: http

    POST /organisation/add HTTP/1.1
    Host: example.com
    Content-Type: application/json

    {
      "name": "New Org",
      "username": "neworg123",
      "password": "securepassword"
    }

Response
~~~~~~~~

Upon successful creation, you'll receive a response similar to:

.. code-block:: json

    {
      "message": "Organisation created successfully"
    }



Retrieve Organisations Endpoint
-------------------------------

This endpoint retrieves a list of organisations from the database.

.. autofunction:: app.main.get_organisations

Example
~~~~~~~

To retrieve a list of organisations, send a GET request to `/organisations`.

.. code-block:: http

    GET /organisations HTTP/1.1
    Host: example.com

Response
~~~~~~~~

Upon successful retrieval, you'll receive a response containing a list of organisations similar to:

.. code-block:: json

    [
      {
        "name": "Org1",
        "username": "org1user",
        "password": "org1password"
      },
      {
        "name": "Org2",
        "username": "org2user",
        "password": "org2password"
      }
    ]

Retrieve Organisation by Name Endpoint
--------------------------------------

This endpoint retrieves an organisation by its name from the database.

.. autofunction:: app.main.get_organisation_by_name

Example
~~~~~~~

To retrieve an organisation by its name, send a GET request to `/organisation/{name}` where `{name}` is the name of the organisation.

.. code-block:: http

    GET /organisation/Org1 HTTP/1.1
    Host: example.com

Response
~~~~~~~~

Upon successful retrieval, you'll receive a response containing the organisation details similar to:

.. code-block:: json

    {
      "name": "Org1",
      "username": "org1user",
      "password": "org1password"
    }

Retrieve Organisation by ID Endpoint
------------------------------------

This endpoint retrieves an organisation by its ID from the database.

.. autofunction:: app.main.get_organisation_by_id

Example
~~~~~~~

To retrieve an organisation by its ID, send a GET request to `/organisation/id/{id}` where `{id}` is the ID of the organisation.

.. code-block:: http

    GET /organisation/id/1 HTTP/1.1
    Host: example.com

Response
~~~~~~~~

Upon successful retrieval, you'll receive a response containing the organisation details similar to:

.. code-block:: json

    {
      "name": "Org1",
      "username": "org1user",
      "password": "org1password"
    }


Delete Organisation Endpoint
-----------------------------

This endpoint deletes an organisation by its ID from the database.

.. autofunction:: app.main.delete_organisation

Example
~~~~~~~

To delete an organisation by its ID, send a DELETE request to `/organisation/delete/{id}` where `{id}` is the ID of the organisation.

.. code-block:: http

    DELETE /organisation/delete/1 HTTP/1.1
    Host: example.com

Response
~~~~~~~~

Upon successful deletion, you'll receive a response similar to:

.. code-block:: json

    {
      "message": "Organisation deleted successfully"
    }

