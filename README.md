# Task Manager API

A simple Flask-based RESTful API for managing tasks with JWT authentication.

---

## Setup Instructions

```bash
git clone <repository_url>
cd task-manager

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt


# Linux / Mac
export FLASK_APP=run.py
export FLASK_ENV=development

# Windows (CMD)
set FLASK_APP=run.py
set FLASK_ENV=development

# Initialize the database
flask db init       # Only once
flask db migrate    # Generate migration scripts
flask db upgrade    # Apply migrations


Run the application
flask run


Access the API at: http://127.0.0.1:5000

Swagger UI documentation: http://127.0.0.1:5000/apidocs

Notes

Use /auth/register to create a user and /auth/login to get a JWT token.

Include the JWT token in the Authorization header (Bearer <token>) for all /tasks endpoints.

Only the authenticated user can manage their own tasks.
