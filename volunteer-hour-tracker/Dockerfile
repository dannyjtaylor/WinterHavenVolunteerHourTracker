FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/main.py ./main.py
COPY app/static ./app/static
COPY app/templates ./app/templates

EXPOSE 8000

CMD ["python", "main.py"]