FROM python:3-alpine

RUN mkdir /code
WORKDIR /code

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code

ENTRYPOINT python main.py