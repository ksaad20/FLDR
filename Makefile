.PHONY: install lint format test security check clean docker

PYTHON := python3
PIP := $(PYTHON) -m pip

install:
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

lint:
	ruff check .
	flake8 .

format:
	black .
	ruff check . --fix

test:
	pytest -q --tb=short

test-cov:
	pytest -q --tb=short --cov=fldr --cov-report=term-missing --cov-report=html

security:
	bandit -r fldr
	safety check

typecheck:
	mypy fldr

check: format lint typecheck test security
	@echo "✅ All checks passed"

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t fldr:latest .

docker-run:
	docker run -p 8000:8000 fldr:latest
