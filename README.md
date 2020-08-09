# company-model

A simple REST service with miminal GUI written in [Django](https://www.djangoproject.com/) with Python 3.8.

## Native setup to run locally

Install Python 3.8 or an enviroment manager of your choice. Install pip.

Run (in your Python 3.8 environment)

```bash
python -m pip install -r requirements.txt
```

Start the service

```bash
python manage.py runserver
```

## Docker

Install [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).

Run with `docker-compose`

```bash
docker-compose up
```

Or with raw docker

```bash
docker build --tag company-model-service:1.0 .
docker run -d company-model-service:1.0
```
