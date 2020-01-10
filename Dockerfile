FROM python:3.7-slim-buster

COPY ./requirements-docker.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./naomi_bot /app