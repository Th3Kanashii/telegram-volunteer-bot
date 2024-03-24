package_dir := bot

.PHONY: install
install:
	python3 -m venv venv
	. venv/bin/activate && \
	pip install -r requirements.txt -r dev-requirements.txt

.PHONY: lint
lint:
	black --check $(package_dir)
	ruff $(package_dir)
	mypy $(package_dir) --strict

.PHONY: reformat
reformat:
	black $(package_dir)
	ruff $(package_dir) --fix

.PHONY: migration
migration:
	alembic revision --autogenerate -m $(message) --rev-id $(rev_id)

.PHONY: migrate
	alembic upgrade head

.PHONY: app-build
app-build:
	docker-compose build

.PHONY: app-run
app-run:
	docker-compose stop
	docker-compose up -d --remove-orphans

.PHONY: app-stop
app-stop:
	docker-compose stop

.PHONY: app-down
app-down:
	docker-compose down

.PHONY: app-destroy
app-destroy:
	docker-compose down -v --remove-orphans
