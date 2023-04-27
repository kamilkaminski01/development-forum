#!/bin/bash

echo "Collecting static files"
python manage.py collectstatic --no-input

echo "Starting server"
gunicorn -b 0.0.0.0 -p 80 app.wsgi:application

exec "$@"
