#!/usr/bin/env bash

rm -r eventsoc/migrations
rm db.sqlite3

python manage.py makemigrations eventsoc
python manage.py migrate

python populate_eventsoc.py

python manage.py runserver
