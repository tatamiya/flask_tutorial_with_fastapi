FROM python:3.9-alpine

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry
