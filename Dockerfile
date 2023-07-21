FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir /Traders

WORKDIR /Traders

ADD . /Traders

RUN pip install -r requirements.txt
