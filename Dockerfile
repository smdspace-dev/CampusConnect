# Backend stage
FROM python:3.10-slim as backend-builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY backend/ ./backend
WORKDIR /app/backend

RUN python manage.py collectstatic --noinput || true
RUN python manage.py migrate || true

# Final image
FROM python:3.10-slim
WORKDIR /app
COPY --from=backend-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY backend/ ./backend
WORKDIR /app/backend
ENV DJANGO_SETTINGS_MODULE=backend.settings
EXPOSE 8000
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
