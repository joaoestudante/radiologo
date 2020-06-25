FROM python:3.8-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code/src/
RUN pip install pipenv
RUN apt-get update && apt-get install -y \
    vim \
    pandoc \
    texlive-xetex

COPY . /code/

RUN pipenv install --deploy --ignore-pipfile

ENTRYPOINT ["./launch_backend.sh"]