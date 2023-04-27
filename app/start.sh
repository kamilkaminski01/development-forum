#!/bin/bash

echo "Collecting static files"
python manage.py collectstatic --no-input

echo "Migrating"
python manage.py migrate

echo "Starting server"
gunicorn -b 0.0.0.0 -p 8000 app.wsgi:application

exec "$@"
