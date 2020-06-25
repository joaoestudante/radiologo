<h1 style="text-align:center;">Radiólogo</h1>

Built with ***Vue.js*** and ***Django***

## About

A web app supporting:

* uploads to servers for emission management and archiving
* auto emission audio normalization and trimming, with email alerts
* download of previously uploaded programs
* management and registration of users and programs

## Requirements
```
python 3.8
Redis
sqlite3
ffmpeg
pandoc
xetex/XeLaTeX
```
Check [`backend/Pipfile`](https://github.com/joaoestudante/radiologo/blob/master/backend/Pipfile) for the most up to date python packages.


## Installation

### Docker :whale:
* `cd` into the root directory.
* Build image and start in the background:
  - `docker-compose build`
  - `docker-compose up -d`
* Check that the expected services are running:
  - `docker ps` or `docker-compose ps`


### Traditional
Start by installing `pipenv`:
```
pip3 install pipenv
```

Install all the required packages in the backend:

```
cd backend
pipenv install
```

Apply migrations and run the server:

```
pipenv shell
cd src
python manage.py migrate
python manage.py runserver
```


## Contributing



## License





