PYTHON ?= python3
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python

.PHONY: help bootstrap migrate init-admin run check docker-up docker-down docker-logs docker-init clean

help:
	@echo "bootstrap    create .venv and copy .env.example to .env"
	@echo "migrate      run database migrations"
	@echo "init-admin   create or reset the blog administrator"
	@echo "run          migrate and start Django development server"
	@echo "docker-up    build and start Docker Compose"
	@echo "docker-down  stop Docker Compose"
	@echo "docker-init  create administrator inside the web container"

.venv/bin/python: requirements.txt
	python3 -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

.env:
	cp .env.example .env
	@echo "Created .env. Review it before starting the project."

bootstrap: .venv/bin/python .env
	@$(VENV_PYTHON) -m django --version

migrate: bootstrap
	$(VENV_PYTHON) manage.py migrate

init-admin: migrate
	$(VENV_PYTHON) manage.py init_admin

run: migrate
	$(VENV_PYTHON) manage.py runserver 0.0.0.0:8000

check: bootstrap
	$(VENV_PYTHON) manage.py check

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f web

docker-init:
	docker compose exec web python manage.py init_admin

clean:
	rm -rf $(VENV)
