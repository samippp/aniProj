FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \ PYTHONUNBUFFERED=1 

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install pipenv

COPY ./Pipfile ./Pipfile.lock /app/

RUN pipenv install --system --deploy --ignore-pipfile
COPY . /app/

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]