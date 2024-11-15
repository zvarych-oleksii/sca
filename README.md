# Spy Cat Agency API
A Django REST Framework (DRF) application for managing spy cats, their missions, and associated targets.

## Features
Manage spy cats (CRUD operations with breed validation via TheCatAPI).
Create and assign missions with targets.
Update mission targets (mark as completed, update notes).
Prevent updates to notes if a mission or target is completed.
Automatically mark missions as completed when all targets are done.
Prerequisites
Before starting the project, ensure you have the following installed:

Python (>= 3.8)
pip (Python package installer)
A database (SQLite by default, or PostgreSQL for production)
Setup and Installation
Follow these steps to get the project up and running.

1. Clone the Repository
```bash
git clone <repository-url>
cd sca_project
```
2. Create a Virtual Environment

```bash
python -m venv venv
```
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```
4. Configure the Environment

Create a .env file in the root directory and add the following (update values as needed):
```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

For production, set DEBUG=False and update ALLOWED_HOSTS accordingly.

5. Migrate the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Run the Development Server

```bash
python manage.py runserver
```

## API Endpoints
Spy Cats
- POST /api/cats/ - Create a new spy cat.
- GET /api/cats/ - List all spy cats.
- GET /api/cats/{id}/ - Retrieve a specific spy cat.
- PATCH /api/cats/{id}/ - Update a spy cat (e.g., salary).
- DELETE /api/cats/{id}/ - Delete a spy cat.
Missions
- POST /api/missions/ - Create a mission with targets.
- GET /api/missions/ - List all missions.
- GET /api/missions/{id}/ - Retrieve a specific mission.
- PATCH /api/missions/{id}/ - Assign a cat to a mission.
- PATCH /api/missions/{id}/complete_target/ - Mark a target as completed.
- PATCH /api/missions/{id}/update_notes/ - Update notes for a target.
- DELETE /api/missions/{id}/ - Delete a mission (only if unassigned).