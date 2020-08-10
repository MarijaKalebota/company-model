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
    - gets node with ID 1

    ```python
    requests.post("http://127.0.0.1:8000/company_model_manager/api/v1/nodes/6/", data={"new_parent_id":5})
    ```
    - modifies the parent of node with ID=6 - sets it to the node with ID=5 if that node is not among its descendants

* **/api/v1/nodes/<node_id>/descendants**

    ```python
    requests.get("http://127.0.0.1:8000/company_model_manager/api/v1/nodes/1/descendants/")
    ```

    - gets all descendants of node with ID=1
