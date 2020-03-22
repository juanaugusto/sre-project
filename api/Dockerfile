FROM python:3.8

RUN mkdir /app

COPY requirements.txt /app

RUN cat /app/requirements.txt

RUN pip install -r /app/requirements.txt

ENV PYTHONPATH /app
