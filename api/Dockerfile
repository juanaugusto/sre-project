FROM python:3.8

RUN apt-get update

RUN apt-get install rsyslog -y

RUN mkdir /app

COPY requirements.txt /app

RUN cat /app/requirements.txt

RUN pip install -r /app/requirements.txt