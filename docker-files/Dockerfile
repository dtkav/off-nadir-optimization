FROM ubuntu:trusty

RUN apt-get update && apt-get install --yes \
    python-dev \
    python-pip

RUN pip install \
    pytest

COPY . /app
WORKDIR /app

