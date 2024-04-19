FROM python:3.11-alpine AS crud

COPY ./ ./app/
WORKDIR /app
RUN pip install poetry
RUN poetry install --no-root
