FROM python:3.8.5-alpine

ADD requirements.txt /deps/
RUN python -m pip install -r /deps/requirements.txt

ADD company_model_site /src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# TODO move to a webserver https://docs.djangoproject.com/en/3.1/intro/tutorial01/
EXPOSE 8000
CMD python /src/manage.py runserver 0.0.0.0:8000

