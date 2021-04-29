FROM python:3.9-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry
