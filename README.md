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

## Run tests

```bash
python manage.py test company_model_manager/
```

## Contribute

After you add or change code, run the test suite, and run both `black` and `isort` to unify the code style:

```bash
black company_model_site/company_model_manager/
isort -rc company_model_site/company_model_manager/
```

# API documentation and examples

- /api/nodes/
```
curl -X GET http://127.0.0.1:8000/company_model_manager/nodes/
```
returns all existing nodes
```
curl -X POST http://127.0.0.1:8000/company_model_manager/nodes/ -d "{"parent_id":1}
```

curl -X GET http://127.0.0.1:8000/company_model_manager/nodes/

curl -X POST http://127.0.0.1:8000/company_model_manager/nodes/5/descendants/ -d "{"parent_id":1}

