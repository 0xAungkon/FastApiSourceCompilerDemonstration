ifneq ("$(wildcard .env)","")
	include .env
	export
endif


# Project management
.PHONY: install run migrate makemigrations shell test clean

install:
	pip install -r requirements.txt

run:
	python3 ./manage.py runserver $(or $(HOST),0.0.0.0):$(or $(PORT),8000)

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

shell:
	python3 manage.py shell

test:
	python3 manage.py test

generate-requirements.txt:
	pip freeze > requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf .coverage htmlcov/
	find . -path "./*" -not -path "./.venv/*" -not -path "./venv/*" -path "*/migrations/*.py" -not -name "__init__.py" -delete



lint:
	flake8 .
	black .

check:
	python3 manage.py check

create-admin:
	export DJANGO_SUPERUSER_USERNAME=$(DJANGO_SUPERUSER_USERNAME); export DJANGO_SUPERUSER_EMAIL=$(DJANGO_SUPERUSER_EMAIL) ; export DJANGO_SUPERUSER_PASSWORD=$(DJANGO_SUPERUSER_PASSWORD); python3 ./manage.py createsuperuser --noinput

collectstatic:
	python3 manage.py collectstatic --noinput

# DEV
ENV:
	ln -s .env.sample .env

DBUP:
	docker compose up -d db db_admin 

MSSQL_Manager:
	bash utills/mssql/scripts/mssql_manager.sh

Dummy_Checkinout:
	python3 utills/mssql/scripts/mssql-checkinout.py