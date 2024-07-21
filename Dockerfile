# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /api-flask

COPY . .

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV URL_GSHEET=""

CMD [ "sh" , "-c", "python3 main.py $URL_GSHEET"]
