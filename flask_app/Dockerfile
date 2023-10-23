FROM python:3.11.6-alpine3.18

EXPOSE 8080

WORKDIR /app

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY DS_testing/flask_app/app/main.py /app
COPY DS_testing/flask_app/pyproject.toml /app

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev


CMD ["python", "main.py"]
