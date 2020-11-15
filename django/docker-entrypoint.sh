#!/bin/bash

python /django/manage.py collectstatic --noinput

sleep .10

python /django/manage.py migrate
uwsgi --ini /django/models_estimator_uwsgi.ini
