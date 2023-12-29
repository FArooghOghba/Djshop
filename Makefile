.PHONY: install-pre-commit-hooks
install-pre-commit-hooks:
	pre-commit uninstall && pre-commit install

.PHONY: check-pre-commit
check-pre-commit:
	pre-commit run --all-files

.PHONY: docker-compose-build
docker-compose-build:
	docker compose -f docker-compose.dev.yml up -d

.PHONY: migrations
migrations:
	docker compose -f docker-compose.dev.yml exec django sh -c "python -m src.manage makemigrations"

.PHONY: migrate
migrate:
	docker compose -f docker-compose.dev.yml exec django sh -c "python -m src.manage migrate"

.PHONY: create-superuser
create-superuser:
	docker compose -f docker-compose.dev.yml exec django sh -c "python -m src.manage createsuperuser"

.PHONY: pytest
pytest:
	docker compose -f docker-compose.dev.yml exec django sh -c "python -m pytest -c ./configs/pytest.ini"

.PHONY: mypy
mypy:
	docker compose -f docker-compose.dev.yml exec django sh -c "mypy --config-file ./configs/mypy.ini ./src"

.PHONY: flake8
flake8:
	docker compose -f docker-compose.dev.yml exec django sh -c "flake8 --config=./configs/.flake8 ./src"
