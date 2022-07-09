FROM python:3.10.5-slim-buster

WORKDIR /app

RUN apt -y update
RUN apt -y upgrade

CMD /bin/bash

RUN pip install pipenv
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install

CMD pipenv run deploy