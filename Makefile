.PHONY: test lint format

lint:
	poetry run flake8 --ignore E501 **/*.py
	poetry run black . --check
	poetry run isort . --check-only --profile black
	poetry run mypy . --ignore-missing-imports

format:
	poetry run black .
	poetry run isort . --profile black

test:
	poetry run pytest