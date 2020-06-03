FROM python:3.7-alpine

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r /requirements.txt