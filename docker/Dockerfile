FROM python:3.7-slim-buster

COPY ./docker/requirements-docker.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./naomi_bot /app
COPY docker/bin /usr/local/bin

ENV PORT=80

ENTRYPOINT ["/usr/local/bin/start_bot"]