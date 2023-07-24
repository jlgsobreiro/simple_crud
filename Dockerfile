FROM python:3-alpine AS crud

COPY ./ ./app/
WORKDIR /app
RUN pip install poetry
RUN poetry install --no-root
