# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV URL_GSHEET=""

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "pongtracker.py", "--server.port=8501", "--server.address=0.0.0.0"]