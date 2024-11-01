# College Management System

A full-stack College Management System with Django REST backend and React frontend.

This README explains how to run the project locally, run tests, and optionally use Docker. It includes environment variable examples and common troubleshooting tips.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start (development)](#quick-start-development)
- [Backend Setup (Django)](#backend-setup-detailed)
- [Frontend Setup (React)](#frontend-setup-detailed)
- [Docker (optional)](#docker-optional)
- [Running Tests](#running-tests)
- [Environment Variables](#environment-variable-examples)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [Production Notes](#production-notes)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites
- Git
- Python 3.10+ (3.11 recommended)
- Node.js 16+ and npm (or yarn)
- Optional: Docker & docker-compose
- Recommended tools: VS Code, Postman (API testing)

## Quick Start (development)

1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd college-management
   ```

2. **Backend:**
   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   cp .env.example .env           # edit environment values
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver 8000
   ```

3. **Frontend (in new terminal):**
   ```bash
   cd frontend
   cp .env.example .env           # update REACT_APP_API_URL if needed
   npm install
   npm start
   ```

4. **Visit:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/

## Backend Setup (detailed)

1. **Activate venv, install dependencies:**
   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Environment:**
   Copy `backend/.env.example` to `backend/.env` and edit values.

3. **Database:**
   Default local: sqlite. For production prefer PostgreSQL and set DATABASE_URL accordingly.

4. **Migrations & static:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic  # optional for production/serving static
   ```

5. **Create admin user:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver 8000
   ```

## Frontend Setup (detailed)

1. **Copy .env and install:**
   ```bash
   cd frontend
   cp .env.example .env
   npm install
   ```

2. **Development server:**
   ```bash
   npm start
   ```

3. **Production build:**
   ```bash
   npm run build
   ```

To serve the build via Django, configure STATICFILES_DIRS or copy `frontend/build` into backend static folder. The provided Docker setup may already handle that.

## Docker (optional)

Build and run (if docker-compose.yml is present):
```bash
docker-compose up --build
```

Services will be accessible on ports defined in docker-compose.yml.

## Running Tests

**Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py test
# or if pytest included:
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

## Environment variable examples

### backend/.env.example
```ini
# Django environment variables
SECRET_KEY=replace-me-with-a-strong-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
# Or for PostgreSQL:
# DATABASE_URL=postgres://USER:PASSWORD@db:5432/your_db_name

# Email (for local dev you can use console email backend)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True

# JWT & OAuth
JWT_SECRET_KEY=replace-with-jwt-secret
GOOGLE_OAUTH_CLIENT_ID=your-google-oauth-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-oauth-client-secret
```

### frontend/.env.example
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
REACT_APP_GOOGLE_API_KEY=your-google-api-key
```

## Common Issues & Troubleshooting

- **CORS Errors**: Add your frontend origin to CORS_ALLOWED_ORIGINS in backend settings.
- **Static files missing**: run `collectstatic` and configure WhiteNoise or a static file server.
- **Email not sending**: use console backend for local testing or configure Mailtrap/Gmail correctly.
- **Database connection errors**: verify DATABASE_URL and that DB container/service is running for Postgres.
- **Port conflicts**: change the runserver port with `python manage.py runserver 0.0.0.0:PORT`.
- **JWT auth issues**: check token expiration settings and refresh token implementation.
- **If migrations fail**: check installed apps and circular migrations; run makemigrations for individual apps.

## Useful Commands

- **Apply a new migration:**
  ```bash
  python manage.py makemigrations && python manage.py migrate
  ```

- **Create fixtures or load initial data:**
  ```bash
  python manage.py loaddata initial_data.json
  ```

- **Open Django admin:**
  http://localhost:8000/admin/ (use superuser credentials)

## Production Notes

- Switch `DEBUG=False` and set `ALLOWED_HOSTS`.
- Use HTTPS and secure cookie settings.
- Use PostgreSQL or managed database for production.
- Use Gunicorn + Nginx (or Docker multi-stage) and WhiteNoise or CDN for static assets.
- Set strong `SECRET_KEY` stored in environment variables.
- Configure proper email SMTP credentials.
- Rotate OAuth credentials and JWT secrets regularly.

## Security Checklist (before production)

- [ ] Set `DEBUG=False`
- [ ] Use a strong `SECRET_KEY` stored in environment variables
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS and secure cookies
- [ ] Use a production-grade DB (Postgres) and RDS-like managed solutions
- [ ] Configure proper email SMTP credentials
- [ ] Rotate OAuth credentials and JWT secrets regularly

## Contributing

1. Create issues for problems or feature requests.
2. Fork the repository, create a branch per feature/fix.
3. Open a PR describing changes and tests.

## License

Replace with your chosen license, e.g., MIT.
