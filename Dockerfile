FROM nikolaik/python-nodejs:python3.13-nodejs24-slim

RUN apt update && apt upgrade -y && npm install jsdom atob jsdom-worker node-fetch -g

ADD . /aqua
WORKDIR /aqua
RUN pip install -r requirements.txt --break-system-packages

ENV GUNICORN_WORKER_COUNT=8
ENV GUNICORN_THREADS=8
ENV GUNICORN_TIMEOUT=60
ENV GUNICORN_BACKLOG=16

CMD gunicorn -c gunicorn.config.py app:app
