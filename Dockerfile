FROM python:3.11-slim

RUN apt-get update && apt-get install 

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 3000

CMD ["sh", "-c", "dagster dev -f pipeline.py & uvicorn main:app --host 0.0.0.0 --port 8000"]
