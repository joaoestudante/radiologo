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
COPY requirements.txt $PROJECT_DIR/src/
RUN pip install -r requirements.txt

COPY . $PROJECT_DIR

EXPOSE 8000
STOPSIGNAL SIGINT
CMD python3 manage.py migrate --noinput && gunicorn -b 0.0.0.0:8000 radiologo.wsgi