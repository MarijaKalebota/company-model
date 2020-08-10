FROM python:3.8.5-alpine

ADD requirements.txt /deps/
RUN apk add gcc musl-dev python3-dev
RUN python -m pip install -r /deps/requirements.txt

ADD company_model_site /src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
CMD cd /src; gunicorn company_model_site.wsgi:application --workers 10 --bind 0.0.0.0:8000
