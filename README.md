# Company Model Manager

A simple REST service with a miminal GUI written in [Django](https://www.djangoproject.com/) with Python 3.8.

## Setup to run locally

Install Python 3.8 or an enviroment manager of your choice, and pip.

Run (in your Python 3.8 environment)

```bash
python -m pip install -r requirements.txt
```

There are three ways in which you can start the service:

- for local development purposes

    ```bash
    python manage.py runserver
    ```

- locally with gunicorn

    ```bash
    gunicorn company_model_site.wsgi:application --workers 10
    ```

- using docker-compose

    ```bash
    docker-compose build && docker-compose up
    ```

When the service is up, you can use the API, as well as access the landing page at [http://127.0.0.1:8000/company_model_manager/](http://127.0.0.1:8000/company_model_manager/). This README has chapters with an introduction to both.

### Docker setup

Install [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).

Running the service with `docker-compose`:

```bash
docker-compose build && docker-compose up
```

Or simply with `docker`:

```bash
docker build --tag company-model-service:1.0 .
docker run -d company-model-service:1.0
```

### Running tests

Navigate to the folder where `manage.py` is, and run the following command.

```bash
python manage.py test company_model_manager/
```

## API documentation and examples

The examples below are written in Python 3.8, with `requests` being the only dependency (`pip install requests`). To run these commands, you can use the local Python 3.8 shell while the service is running.

To begin, run `python` (3.8) in the shell of your choosing, then run `import requests`. After that, you can run any of the following commands.

- **/api/v1/nodes/**

    ```python
    requests.get("http://127.0.0.1:8000/company_model_manager/api/v1/nodes/")
    ```
    - returns all existing nodes

    ```python
    requests.post("http://127.0.0.1:8000/company_model_manager/api/v1/nodes/", data={"parent_id":1})
    ```
    - creates a node with parent_id 1 (if such a parent exists)

- **/api/v1/nodes/<node_id>**

    ```python
    requests.get("http://127.0.0.1:8000/company_model_manager/api/v1/nodes/1/")
    ```
    - gets node with ID=1

    ```python
    requests.post("http://127.0.0.1:8000/company_model_manager/api/v1/nodes/6/", data={"new_parent_id":5})
    ```
    - modifies the parent of node with ID=6 - sets it to the node with ID=5 if that node is not among its descendants

* **/api/v1/nodes/<node_id>/descendants**

    ```python
    requests.get("http://127.0.0.1:8000/company_model_manager/api/v1/nodes/1/descendants/")
    ```
    - gets all descendants of node with ID=1

## Short guide through the GUI

After starting the service, open the landing page - [http://127.0.0.1:8000/company_model_manager/](http://127.0.0.1:8000/company_model_manager/).

This will display a link to a list of all nodes that currently exist in Amazing Co, from where you can browse their details and descendants.

Alternatively, you can also append the following URL patterns to the link above to access specific nodes or their descendants.

- **/nodes/\<int:node_id>/**
- **/nodes/\<int:node_id>/descendants/**

## Contribute

After you add or change code, run the test suite, and run both `black` and `isort` to unify the code style:

```bash
black company_model_site/company_model_manager/
isort -rc company_model_site/company_model_manager/
```
