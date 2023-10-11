# Dockerfile

# pull the official docker image
FROM python:3.9-slim

# install latest updates
RUN apt-get update && apt-get -y install
RUN apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .