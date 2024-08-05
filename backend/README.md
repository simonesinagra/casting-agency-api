# Backend - Casting Agency API

## Table of Contents

1. [Local Development Setup](#local-development-setup)
    - [Install Dependencies](#install-dependencies)
    - [Set Up Environment Variables](#set-up-environment-variables)
    - [Set up the Database](#set-up-the-database)
    - [Run the Server](#run-the-server)
2. [API Endpoints](#api-endpoints)
   - [Actors](#actors)
   - [Movies](#movies)
3. [Roles and Permissions](#roles-and-permissions)
4. [Error Handling](#error-handling)
5. [Testing](#testing)

## Local Development Setup

### Install Dependencies

1. **Python 3.12** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a .env file in the root directory and add the following variables:

```text
DB_NAME='casting_agency'
DB_USER='postgres'

AUTH0_DOMAIN = 'dev-nqpsvdwckdv2v7c8.us.auth0.com'
API_AUDIENCE = 'casting-agency-dev'

CASTING_ASSISTANT_TOKEN=your_casting_assistant_token_here
CASTING_DIRECTOR_TOKEN=your_casting_director_token_here
EXECUTIVE_PRODUCER_TOKEN=your_executive_producer_token_here
```

### Set up the Database

With Postgres running, create a `casting_agency` database:

```bash
createdb casting_agency
```

Populate the database using the `casting_agency.psql` file provided. From the `backend` folder in terminal run:

```bash
psql casting_agency < casting_agency.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

The API will be available at `http://localhost:5000`.

## API Endpoints

### Actors

`GET /actors`

**Description:** Retrieve a list of all actors.

**Roles:** Casting Assistant, Casting Director, Executive Producer

**Response:** JSON array of Actor objects.

`GET /actor/<actor_id>`

**Description:** Retrieve a specific actor.

**Roles:** Casting Assistant, Casting Director, Executive Producer

**Response:** Actor object.

`POST /actors`

**Description:** Add a new actor.

**Roles:** Casting Director

**Payload:**

```json
{
    "name": "Actor Name",
    "age": 30,
    "gender": "Male"
}
```

**Response:** The created actor's ID.

`DELETE /actors/<actor_id>`

**Description:** Delete an actor by ID.

**Roles:** Casting Director

**Response:** The deleted actor's ID.

`PATCH /actors/<actor_id>`

**Description:** Update an actor's details.

**Roles:** Casting Director

**Payload:**

```json
{
    "name": "Updated Name",
    "age": 35,
    "gender": "Female"
}
```

**Response:** The patched actor's ID.

### Movies

`GET /movies`

**Description:** Retrieve a list of all movies.

**Roles:** Casting Assistant, Casting Director, Executive Producer

**Response:** JSON array of Movie objects.

`GET /movies/<movie_id>`

**Description:** Retrieve a specific movie.

**Roles:** Casting Assistant, Casting Director, Executive Producer

**Response:** Movie object.

`POST /movies`

**Description:** Add a new movie.

**Roles:** Executive Producer

**Payload:**

```json
{
  "title": "Movie Title",
  "release_date": "YYYY-MM-DD"
}
```

**Response:** The created movie's ID.

`DELETE /movies/<movie_id>`

**Description:** Delete a movie by ID.

**Roles:** Executive Producer

**Response:** The deleted movie's ID.

`PATCH /movies/<movie_id>`

**Description:** Update a movie's details.

**Roles:** Casting Director

**Payload:**

```json
{
  "title": "Updated Title",
  "release_date": "YYYY-MM-DD"
}
```

**Response:** The patched movie's ID.

## Roles and Permissions

The Casting Agency API uses Role-Based Access Control (RBAC) to manage access to various resources. There are three distinct roles, each with specific permissions.

### Casting Assistant

The **Casting Assistant** is the most basic role with read-only access to the data.

- **Permissions**:
  - View details of actors.
  - View details of movies.

- **Use Case**: This role is ideal for someone who needs to access information about actors and movies without the ability to modify or delete any data. For example, this could be an intern or a researcher who needs to review the existing records.

### Casting Director

The **Casting Director** has broader permissions compared to the Casting Assistant. This role can manage actors and update movie information.

- **Permissions**:
  - Inherits all permissions of the **Casting Assistant** role.
  - Add a new actor to the database.
  - Delete an existing actor from the database.
  - Modify details of existing actors (e.g., update name, age, gender).
  - Modify details of existing movies (e.g., update title, release date).

- **Use Case**: This role is suitable for someone responsible for managing the actors and their assignments to different movies. For example, this could be a casting director or a member of the production team who needs to maintain the actor's records and update movie information.

### Executive Producer

The **Executive Producer** has the highest level of access and control over the system.

- **Permissions**:
  - Inherits all permissions of the **Casting Director** role.
  - Add a new movie to the database.
  - Delete an existing movie from the database.

- **Use Case**: This role is for someone who has full control over the production process and the authority to manage both actors and movies. Typically, this would be an executive producer or a senior manager within the organization who oversees the entire production process and has the final say on casting and movie creation.

## Error Handling

- **400 Bad Request:** Returned when required fields are missing in the request payload.

- **404 Not Found:** Returned when a requested resource (actor or movie) is not found.

- **422 Unprocessable:** Returned when a request is unprocessable.

- **AuthError:** Returned when an authentication error occurs.

## Testing

To deploy the tests, run

```bash
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency.psql
python test_flaskr.py
```
