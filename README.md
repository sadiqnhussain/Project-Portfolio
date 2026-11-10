# PortfolioSite

A Django-powered developer portfolio with a server-rendered UI, a REST API, project case studies, and live health monitoring. Portfolio content is managed through Django Admin; public pages and API responses expose published content.

## live project link.
https://sadiqnhussain.onrender.com/

## Features

- Responsive portfolio pages for the home page, projects, profile, and contact information
- Django REST Framework endpoints for portfolio content, projects, and system health
- Interactive API documentation with Swagger UI and ReDoc, generated from an OpenAPI schema
- Project case studies with stack details, architecture notes, and optional deployment health checks
- Admin-managed profile, skills, experience, recommendations, projects, and contact messages
- Resume download tracking and an interactive API Lab
- SQLite for local development and PostgreSQL-ready Docker configuration
- Static-file serving through WhiteNoise

## Technology stack

| Technology            | Purpose                                                                |
| --------------------- | ---------------------------------------------------------------------- |
| Django                | Web framework, routing, templates, ORM, admin, and security middleware |
| Django REST Framework | JSON API views and serializers                                         |
| drf-spectacular       | OpenAPI schema generation, Swagger UI, and ReDoc                       |
| SQLite / PostgreSQL   | Local database / deployment database options                           |
| WhiteNoise            | Serving collected static assets in production-style deployments        |
| Gunicorn              | WSGI application server in the container                               |
| Pillow                | Image field and image processing support                               |
| django-environ        | Environment-based configuration                                        |

## Requirements

- Python 3.12 or newer compatible with the pinned Django range
- pip
- Optional: Docker and Docker Compose for containerized deployment

## Local setup

1. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   # Windows PowerShell: .venv\\Scripts\\Activate.ps1
   # macOS/Linux: source .venv/bin/activate
   ```

2. Install dependencies.

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and review the values. Set a unique `SECRET_KEY`, `DEBUG=True`, and `ALLOWED_HOSTS=localhost,127.0.0.1` for local development. Never commit `.env`. The project defaults to SQLite when `DATABASE_URL` is not set.

4. Apply migrations and create an admin account.

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Start the development server.

   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/`. Manage portfolio content at `/admin/`.

To load the optional demonstration content, run `python manage.py seed_demo` after migrations. Review the command's behavior before using it against a database containing real content.

## API documentation

| Route             | Purpose                                              |
| ----------------- | ---------------------------------------------------- |
| `/api/v1/docs/`   | Swagger UI for exploring API operations              |
| `/api/v1/redoc/`  | ReDoc API reference                                  |
| `/api/v1/schema/` | OpenAPI schema in JSON/YAML format (JSON by default) |

The documentation is generated from the API views and serializers, so the schema reflects the API contract rather than a separately maintained static document.

## Main pages

- `/` — home page
- `/projects/` — project index
- `/projects/<slug>/` — project case study and health details
- `/about/` — profile and experience
- `/contact/` — contact form and direct links
- `/api-lab/` — interactive API Lab
- `/resume/download/` — resume download endpoint
- `/admin/` — content administration

## API routes

- `/api/v1/dashboard/health/` — portfolio infrastructure and monitored project health
- `/api/v1/projects/` — published projects, with optional `featured` and `recent` filters
- `/api/v1/projects/<slug>/` — published project details
- `/api/v1/projects/<slug>/health/` — health information for a published project
- `/api/v1/content/profile/`, `/site/`, `/skills/`, `/experience/`, `/recommendations/`, `/about/` — portfolio content endpoints

All public API routes are rooted at `/api/v1/`. Django Admin remains staff-authenticated; the public portfolio does not require visitor accounts.

## Health monitoring

Configure a project's live URL and, when available, a dedicated health-check URL in Django Admin. Enable health checks and set a timeout appropriate for the deployment. The portfolio infrastructure health endpoint is distinct from individual monitored project statuses, so a monitored external project's outage does not imply the portfolio itself is unavailable.

## Tests

Run the Django test suite with:

```bash
python manage.py test
```

Tests cover key public pages, API responses, error cases, and the OpenAPI documentation routes. Authentication-specific tests are intentionally not included.

## Deployment notes

- Set `DEBUG=False`, a strong `SECRET_KEY`, and an explicit `ALLOWED_HOSTS` value in production.
- Configure `DATABASE_URL` for PostgreSQL when deploying with Docker Compose.
- Run migrations during release and collect static assets with `python manage.py collectstatic --noinput`.
- Persist uploaded media using a durable volume or object storage.

### Feedbacks and Contributions to the project are highly appreciated.
