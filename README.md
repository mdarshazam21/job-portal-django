# Job Portal — Django Backend Project

A full-featured job portal / recruitment platform built with Django, featuring role-based authentication, job postings, applications with resume uploads, a REST API, email notifications, and automated tests.

## Features

- **Custom user authentication** with two roles: Candidate and Recruiter
- **Recruiter workflow**: company profile creation, job posting management
- **Candidate workflow**: browse/search/filter jobs, apply with resume + cover letter, track application status
- **Application management**: recruiters can view applicants and update status (Applied → Shortlisted → Hired/Rejected)
- **Email notifications** sent to candidates when their application status changes
- **REST API** built with Django REST Framework, mirroring all core functionality for external clients
- **Search, filtering, and pagination** on job listings
- **Object-level permissions**: recruiters can only manage their own job postings and applicants
- **Responsive UI** built with custom CSS (Flexbox + CSS Grid, no frontend framework)
- **23 automated tests** covering models, views, and permission logic
- **PostgreSQL** database with environment-based configuration

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL
- **Frontend:** HTML, custom CSS (Flexbox, Grid)
- **Auth:** Django's built-in auth system, extended with a custom User model

## Project Structure
job_portal/
├── accounts/ # Custom User model, auth, company profiles
├── jobs/ # Job posting model, views, API
├── applications/ # Application model, resume uploads, status workflow, API
├── job_portal_project/ # Project settings, root URLs
├── static/css/ # Custom stylesheet
└── templates/ # Shared base template


## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/job-portal.git
   cd job-portal
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   #Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root (see `.env.example` for required variables):
SECRET_KEY=your-secret-key
DB_NAME=job_portal_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432


5. Create a PostgreSQL database named `job_portal_db` (via pgAdmin or `createdb`).

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

9. Visit `http://127.0.0.1:8000/`

## Running Tests

```bash
python manage.py test
```

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/jobs/` | GET, POST | List all active jobs / create a job (recruiters only) |
| `/api/jobs/<id>/` | GET | Retrieve a single job |
| `/api/applications/apply/<job_id>/` | POST | Apply to a job (candidates only) |
| `/api/applications/my-applications/` | GET | List the logged-in candidate's applications |
| `/api/applications/job/<job_id>/applicants/` | GET | List applicants for a job (owning recruiter only) |
| `/api/applications/<id>/status/` | PATCH | Update an application's status (owning recruiter only) |

## Screenshots

*(Add screenshots of the home page, job listings, and application flow here)*

## License

This project is for educational/portfolio purposes.