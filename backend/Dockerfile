FROM python:3.8-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code/src/
RUN pip install pipenv
COPY . /code/
RUN pipenv install --deploy --ignore-pipfile
