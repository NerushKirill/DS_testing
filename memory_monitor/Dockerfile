FROM python:3.11.6-alpine3.18

EXPOSE 8000
WORKDIR /monitor

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY DS_testing/memory_monitor/src/main.py /monitor
COPY DS_testing/memory_monitor/pyproject.toml /monitor

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev


CMD ["python", "main.py"]
