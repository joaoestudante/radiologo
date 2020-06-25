#!/bin/bash
pipenv run python manage.py migrate --noinput
pipenv run gunicorn -b 0.0.0.0:8000 radiologo.wsgi

