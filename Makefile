.PHONY: test lint security docker

test:
	python -m pytest --cov=app --cov-report=term

lint:
	ruff check .

security:
	bandit -c pyproject.toml -r app
	pip-audit -r requirements.txt

docker:
	docker build -t minirisk:local .
