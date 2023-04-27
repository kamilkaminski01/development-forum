build:
	docker build -t development-forum .

start:
	docker run -p 8000:8000 --name development-forum development-forum

run:
	cd app/ && python manage.py runserver

migrations:
	cd app/ && python manage.py makemigrations

migrate:
	cd app/ && python manage.py migrate

superuser:
	cd app/ && python manage.py createsuperuser

check:
	cd app/ && black . && isort . && mypy . && flake8 .

flush:
	cd app/ && python manage.py flush

initial-data:
	cd app/ && python manage.py initialize_data

pytest:
	cd app/ && python -m pytest

pytest-module:
	cd app/ && python -m pytest $(module)/
