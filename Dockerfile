# Установка зависимостей poetry и экспорт в requirements.txt
FROM python:3.12-alpine AS builder
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry==1.8.0
RUN poetry export --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.12-alpine
WORKDIR /app
COPY --from=builder requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
