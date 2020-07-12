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
* Rename the `/backend/src/radiologo/resources/application.properties.example` to `application.properties` (remove the `.example`) and fill the missing fields correctly.
* Build image and start in the background:
  - `docker-compose build`
  - `docker-compose up -d`
* Check that the expected services are running:
  - `docker ps` or `docker-compose ps`

#### Docker: First time DB configuration

1. Create a superuser
  - ` sudo docker exec -it radiologo-backend /bin/sh -c 'pipenv run python manage.py createsuperuser' `
2. Set superuser password (properly)
  - Open the shell: 
      ` sudo docker exec -it radiologo-backend /bin/sh -c 'pipenv run python manage.py shell' ` 
  - Run the commands:
      - ``` 
        from users.models.user import CustomUser
        u = CustomUser.objects.get(pk=1)
        u.set_password("a tua password")
        u.save()
        ```


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





