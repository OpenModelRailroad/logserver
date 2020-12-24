FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY console ./
COPY logserver ./
COPY static ./
COPY templates ./
COPY manage.py ./