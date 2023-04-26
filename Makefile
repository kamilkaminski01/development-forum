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
