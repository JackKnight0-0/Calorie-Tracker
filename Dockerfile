FROM python:3.11.7-slim-bullseye

RUN apt-get update && apt-get install -y sudo


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR ./CalorieTracker

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .