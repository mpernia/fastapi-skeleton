.PHONY: help build up down logs ps test lint format migrate migrate-down clean install dev docker-test setup env seed

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml
PYTHON = python3
PIP = pip3

help: ## Show this help message
	@echo 'Usage:'
	@echo '  make <target>'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

env: ## Create .env file if it doesn't exist
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from .env.example"; \
	fi

install: ## Install development dependencies
	$(PIP) install -r requirements.txt
	pre-commit install

build: env ## Build docker images
	$(DOCKER_COMPOSE) build

up: env ## Start all docker containers
	$(DOCKER_COMPOSE) up -d

down: ## Stop all docker containers
	$(DOCKER_COMPOSE) down

logs: ## View docker container logs
	$(DOCKER_COMPOSE) logs -f

ps: ## List docker containers
	$(DOCKER_COMPOSE) ps

wait-for-db: ## Wait for database to be ready
	@echo "Waiting for database to be ready..."
	@until docker-compose exec db pg_isready -h localhost -p 5432 -U user; do \
		echo "Database is unavailable - sleeping"; \
		sleep 2; \
	done

test: ## Run tests
	$(DOCKER_COMPOSE) exec api pytest

lint: ## Run linting
	$(DOCKER_COMPOSE) exec api black .
	$(DOCKER_COMPOSE) exec api flake8 .
	$(DOCKER_COMPOSE) exec api isort .
	$(DOCKER_COMPOSE) exec api mypy .

format: ## Format code
	$(DOCKER_COMPOSE) exec api black .
	$(DOCKER_COMPOSE) exec api isort .

seed:
	@echo "Running seeders..."
	docker-compose exec api python -c "from api.seeders.run_seeders import run_seeders; run_seeders()"

migrate: wait-for-db ## Run database migrations
	@echo "Waiting for database to be ready..."
	@until docker-compose exec db pg_isready -h localhost -p 5432; do sleep 1; done
	docker-compose exec api alembic upgrade head
	@make seed

migrate-down: ## Rollback last database migration
	$(DOCKER_COMPOSE) exec api alembic downgrade -1

clean: ## Remove all build, test, coverage and Python artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

dev: ## Start development server
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

docker-test: ## Run tests in a new container
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up \
		--build --abort-on-container-exit --exit-code-from api

setup: env ## Initial setup of the project
	@echo "Setting up the project..."
	$(MAKE) build
	$(MAKE) up
	@echo "Waiting for services to start..."
	@sleep 10
	$(MAKE) migrate
	@echo "Setup complete! The API is now running at http://localhost:$${API_PORT:-8000}"
	@echo "Documentation available at:"
	@echo "  - Swagger UI: http://localhost:$${API_PORT:-8000}/docs"
	@echo "  - ReDoc: http://localhost:$${API_PORT:-8000}/redoc"
	@echo "Monitoring:"
	@echo "  - Prometheus: http://localhost:$${PROMETHEUS_PORT:-9090}"
	@echo "  - Grafana: http://localhost:$${GRAFANA_PORT:-3000}"

rerun:
	$(MAKE) down && docker-compose down --volumes --remove-orphans && $(MAKE) setup