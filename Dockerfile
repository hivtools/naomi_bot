FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./requirements-docker.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./naomi_bot /app