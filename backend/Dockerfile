FROM ubuntu:20.10

RUN DEBIAN_FRONTEND="noninteractive" apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y \
    python3.8 \
    vim \
    pandoc \
    texlive-xetex \
    python3-pip \
    fonts-ubuntu \
    ffmpeg

ARG PROJECT=radiologo
ARG PROJECT_DIR=/var/www/${PROJECT}
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR/src

RUN pip install pipenv

COPY . $PROJECT_DIR

RUN pipenv install --deploy --ignore-pipfile

EXPOSE 8000
STOPSIGNAL SIGINT
CMD pipenv run python manage.py migrate --noinput && pipenv run gunicorn -b 0.0.0.0:8000 radiologo.wsgi