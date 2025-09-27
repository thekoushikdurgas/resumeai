# Resume/CV AI - Makefile
# Build automation and development commands

# =============================================================================
# Variables
# =============================================================================

# Project Information
PROJECT_NAME = resumeai
VERSION = 1.0.0
PYTHON_VERSION = 3.11

# Docker Configuration
DOCKER_IMAGE = resumeai
DOCKER_TAG = latest
DOCKER_REGISTRY = your-registry.com

# Application Configuration
APP_PORT = 8501
APP_HOST = localhost

# Database Configuration
POSTGRES_DB = resume_ai_db
POSTGRES_USER = resume_ai
POSTGRES_PASSWORD = resume_ai_password

# Redis Configuration
REDIS_PASSWORD = redis_password

# Directories
SRC_DIR = .
BUILD_DIR = build
DIST_DIR = dist
DOCS_DIR = docs
TESTS_DIR = tests
LOGS_DIR = logs

# Python Configuration
PYTHON = python3
PIP = pip3
VENV_DIR = venv
VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_PIP = $(VENV_DIR)/bin/pip

# Docker Compose
COMPOSE_FILE = docker-compose.yml
COMPOSE_DEV_FILE = docker-compose.override.yml

# =============================================================================
# Default Target
# =============================================================================
.DEFAULT_GOAL := help

# =============================================================================
# Help Target
# =============================================================================
.PHONY: help
help: ## Show this help message
	@echo "Resume/CV AI - Available Commands"
	@echo "=================================="
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "For more information, see README.md"

# =============================================================================
# Development Setup
# =============================================================================

.PHONY: setup
setup: ## Initial project setup
	@echo "Setting up Resume/CV AI project..."
	@mkdir -p $(LOGS_DIR) $(BUILD_DIR) $(DIST_DIR)
	@mkdir -p cache temp uploads downloads
	@mkdir -p chroma_db faiss_index
	@echo "Project directories created"

.PHONY: install
install: ## Install Python dependencies
	@echo "Installing Python dependencies..."
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed successfully"

.PHONY: install-dev
install-dev: ## Install development dependencies
	@echo "Installing development dependencies..."
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy ipython jupyter
	@echo "Development dependencies installed"

.PHONY: venv
venv: ## Create virtual environment
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created at $(VENV_DIR)"
	@echo "Activate with: source $(VENV_DIR)/bin/activate"

.PHONY: venv-install
venv-install: venv ## Create venv and install dependencies
	@echo "Installing dependencies in virtual environment..."
	$(VENV_PIP) install --upgrade pip setuptools wheel
	$(VENV_PIP) install -r requirements.txt
	@echo "Dependencies installed in virtual environment"

# =============================================================================
# Application Commands
# =============================================================================

.PHONY: run
run: ## Run the application locally
	@echo "Starting Resume/CV AI application..."
	streamlit run main.py --server.port=$(APP_PORT) --server.address=$(APP_HOST)

.PHONY: run-dev
run-dev: ## Run application in development mode
	@echo "Starting Resume/CV AI in development mode..."
	streamlit run main.py --server.port=$(APP_PORT) --server.address=$(APP_HOST) --server.runOnSave=true

.PHONY: run-prod
run-prod: ## Run application in production mode
	@echo "Starting Resume/CV AI in production mode..."
	streamlit run main.py --server.port=$(APP_PORT) --server.address=0.0.0.0 --server.headless=true

# =============================================================================
# Docker Commands
# =============================================================================

.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "Docker image built successfully"

.PHONY: docker-build-dev
docker-build-dev: ## Build development Docker image
	@echo "Building development Docker image..."
	docker build --target development -t $(DOCKER_IMAGE):dev .
	@echo "Development Docker image built successfully"

.PHONY: docker-run
docker-run: ## Run Docker container
	@echo "Running Docker container..."
	docker run -p $(APP_PORT):8501 \
		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
		-e GOOGLE_API_KEY=$(GOOGLE_API_KEY) \
		-e ANTHROPIC_API_KEY=$(ANTHROPIC_API_KEY) \
		$(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: docker-run-dev
docker-run-dev: ## Run development Docker container
	@echo "Running development Docker container..."
	docker run -p $(APP_PORT):8501 \
		-v $(PWD):/app \
		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
		$(DOCKER_IMAGE):dev

# =============================================================================
# Docker Compose Commands
# =============================================================================

.PHONY: compose-up
compose-up: ## Start all services with docker-compose
	@echo "Starting services with docker-compose..."
	docker-compose up -d
	@echo "Services started successfully"

.PHONY: compose-up-dev
compose-up-dev: ## Start development services
	@echo "Starting development services..."
	docker-compose up -d
	@echo "Development services started"

.PHONY: compose-up-prod
compose-up-prod: ## Start production services
	@echo "Starting production services..."
	docker-compose --profile production up -d
	@echo "Production services started"

.PHONY: compose-up-monitoring
compose-up-monitoring: ## Start services with monitoring
	@echo "Starting services with monitoring..."
	docker-compose --profile monitoring up -d
	@echo "Services with monitoring started"

.PHONY: compose-down
compose-down: ## Stop all services
	@echo "Stopping all services..."
	docker-compose down
	@echo "Services stopped"

.PHONY: compose-down-volumes
compose-down-volumes: ## Stop services and remove volumes
	@echo "Stopping services and removing volumes..."
	docker-compose down -v
	@echo "Services stopped and volumes removed"

.PHONY: compose-logs
compose-logs: ## View logs for all services
	@echo "Viewing logs for all services..."
	docker-compose logs -f

.PHONY: compose-logs-app
compose-logs-app: ## View logs for application service
	@echo "Viewing application logs..."
	docker-compose logs -f resumeai-app

.PHONY: compose-restart
compose-restart: ## Restart all services
	@echo "Restarting all services..."
	docker-compose restart
	@echo "Services restarted"

.PHONY: compose-rebuild
compose-rebuild: ## Rebuild and restart services
	@echo "Rebuilding and restarting services..."
	docker-compose build --no-cache
	docker-compose up -d
	@echo "Services rebuilt and restarted"

# =============================================================================
# Database Commands
# =============================================================================

.PHONY: db-init
db-init: ## Initialize database
	@echo "Initializing database..."
	docker-compose exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "CREATE EXTENSION IF NOT EXISTS vector;"
	@echo "Database initialized"

.PHONY: db-migrate
db-migrate: ## Run database migrations
	@echo "Running database migrations..."
	$(PYTHON) -m alembic upgrade head
	@echo "Database migrations completed"

.PHONY: db-reset
db-reset: ## Reset database (WARNING: This will delete all data)
	@echo "WARNING: This will delete all data in the database!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	docker-compose down -v
	docker-compose up -d postgres
	@echo "Database reset completed"

.PHONY: db-backup
db-backup: ## Backup database
	@echo "Backing up database..."
	@mkdir -p backups
	docker-compose exec postgres pg_dump -U $(POSTGRES_USER) $(POSTGRES_DB) > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backup completed"

# =============================================================================
# Testing Commands
# =============================================================================

.PHONY: test
test: ## Run tests
	@echo "Running tests..."
	pytest $(TESTS_DIR) -v --cov=$(SRC_DIR) --cov-report=html --cov-report=term
	@echo "Tests completed"

.PHONY: test-unit
test-unit: ## Run unit tests only
	@echo "Running unit tests..."
	pytest $(TESTS_DIR)/unit -v
	@echo "Unit tests completed"

.PHONY: test-integration
test-integration: ## Run integration tests
	@echo "Running integration tests..."
	pytest $(TESTS_DIR)/integration -v
	@echo "Integration tests completed"

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "Running tests with coverage..."
	pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/"

# =============================================================================
# Code Quality Commands
# =============================================================================

.PHONY: lint
lint: ## Run linting
	@echo "Running linting..."
	flake8 $(SRC_DIR) --max-line-length=100 --exclude=venv,__pycache__,.git
	@echo "Linting completed"

.PHONY: format
format: ## Format code with black
	@echo "Formatting code..."
	black $(SRC_DIR) --line-length=100 --exclude=venv
	@echo "Code formatting completed"

.PHONY: type-check
type-check: ## Run type checking with mypy
	@echo "Running type checking..."
	mypy $(SRC_DIR) --ignore-missing-imports
	@echo "Type checking completed"

.PHONY: security-check
security-check: ## Run security checks
	@echo "Running security checks..."
	bandit -r $(SRC_DIR) -f json -o security-report.json
	safety check
	@echo "Security checks completed"

.PHONY: quality
quality: lint format type-check security-check ## Run all code quality checks
	@echo "All code quality checks completed"

# =============================================================================
# Documentation Commands
# =============================================================================

.PHONY: docs
docs: ## Generate documentation
	@echo "Generating documentation..."
	@mkdir -p $(DOCS_DIR)/build
	sphinx-build -b html $(DOCS_DIR) $(DOCS_DIR)/build
	@echo "Documentation generated in $(DOCS_DIR)/build/"

.PHONY: docs-serve
docs-serve: docs ## Generate and serve documentation
	@echo "Serving documentation at http://localhost:8000"
	cd $(DOCS_DIR)/build && python -m http.server 8000

# =============================================================================
# Cleanup Commands
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	rm -rf $(BUILD_DIR) $(DIST_DIR)
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	rm -rf *.egg-info .eggs
	@echo "Build artifacts cleaned"

.PHONY: clean-docker
clean-docker: ## Clean Docker images and containers
	@echo "Cleaning Docker artifacts..."
	docker-compose down -v
	docker system prune -f
	docker image prune -f
	@echo "Docker artifacts cleaned"

.PHONY: clean-logs
clean-logs: ## Clean log files
	@echo "Cleaning log files..."
	rm -rf $(LOGS_DIR)/*
	@echo "Log files cleaned"

.PHONY: clean-cache
clean-cache: ## Clean cache files
	@echo "Cleaning cache files..."
	rm -rf cache/* temp/* __pycache__ .pytest_cache
	@echo "Cache files cleaned"

.PHONY: clean-all
clean-all: clean clean-docker clean-logs clean-cache ## Clean everything
	@echo "All cleanup completed"

# =============================================================================
# Deployment Commands
# =============================================================================

.PHONY: deploy-dev
deploy-dev: ## Deploy to development environment
	@echo "Deploying to development environment..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	@echo "Development deployment completed"

.PHONY: deploy-prod
deploy-prod: ## Deploy to production environment
	@echo "Deploying to production environment..."
	docker-compose --profile production up -d
	@echo "Production deployment completed"

.PHONY: deploy-staging
deploy-staging: ## Deploy to staging environment
	@echo "Deploying to staging environment..."
	docker-compose --profile staging up -d
	@echo "Staging deployment completed"

# =============================================================================
# Monitoring Commands
# =============================================================================

.PHONY: monitor
monitor: ## Start monitoring services
	@echo "Starting monitoring services..."
	docker-compose --profile monitoring up -d
	@echo "Monitoring services started"
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3000"

.PHONY: logs
logs: ## View application logs
	@echo "Viewing application logs..."
	docker-compose logs -f resumeai-app

.PHONY: status
status: ## Check service status
	@echo "Checking service status..."
	docker-compose ps

# =============================================================================
# Utility Commands
# =============================================================================

.PHONY: shell
shell: ## Open shell in application container
	@echo "Opening shell in application container..."
	docker-compose exec resumeai-app bash

.PHONY: db-shell
db-shell: ## Open database shell
	@echo "Opening database shell..."
	docker-compose exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

.PHONY: redis-cli
redis-cli: ## Open Redis CLI
	@echo "Opening Redis CLI..."
	docker-compose exec redis redis-cli -a $(REDIS_PASSWORD)

.PHONY: health
health: ## Check application health
	@echo "Checking application health..."
	curl -f http://$(APP_HOST):$(APP_PORT)/_stcore/health || echo "Application is not healthy"

# =============================================================================
# Development Workflow
# =============================================================================

.PHONY: dev-setup
dev-setup: setup install-dev compose-up-dev ## Complete development setup
	@echo "Development environment setup completed"
	@echo "Application available at: http://$(APP_HOST):$(APP_PORT)"

.PHONY: dev-reset
dev-reset: compose-down-volumes compose-up-dev ## Reset development environment
	@echo "Development environment reset completed"

.PHONY: dev-update
dev-update: compose-rebuild ## Update development environment
	@echo "Development environment updated"

# =============================================================================
# Production Workflow
# =============================================================================

.PHONY: prod-setup
prod-setup: setup install compose-up-prod ## Complete production setup
	@echo "Production environment setup completed"

.PHONY: prod-deploy
prod-deploy: docker-build compose-up-prod ## Deploy to production
	@echo "Production deployment completed"

# =============================================================================
# CI/CD Commands
# =============================================================================

.PHONY: ci-test
ci-test: ## Run CI tests
	@echo "Running CI tests..."
	make quality
	make test
	@echo "CI tests completed"

.PHONY: ci-build
ci-build: ## Build for CI
	@echo "Building for CI..."
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "CI build completed"

# =============================================================================
# Environment Commands
# =============================================================================

.PHONY: env-check
env-check: ## Check environment variables
	@echo "Checking environment variables..."
	@echo "OPENAI_API_KEY: $(if $(OPENAI_API_KEY),set,not set)"
	@echo "GOOGLE_API_KEY: $(if $(GOOGLE_API_KEY),set,not set)"
	@echo "ANTHROPIC_API_KEY: $(if $(ANTHROPIC_API_KEY),set,not set)"

.PHONY: env-setup
env-setup: ## Setup environment variables
	@echo "Setting up environment variables..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file from template"; fi
	@echo "Please edit .env file with your actual values"

# =============================================================================
# Backup and Restore
# =============================================================================

.PHONY: backup
backup: ## Create full backup
	@echo "Creating full backup..."
	@mkdir -p backups
	make db-backup
	tar -czf backups/full_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz \
		--exclude=venv --exclude=__pycache__ --exclude=.git \
		--exclude=backups --exclude=logs .
	@echo "Full backup completed"

.PHONY: restore
restore: ## Restore from backup (requires BACKUP_FILE variable)
	@echo "Restoring from backup: $(BACKUP_FILE)"
	@if [ -z "$(BACKUP_FILE)" ]; then echo "Please specify BACKUP_FILE=path/to/backup.tar.gz"; exit 1; fi
	tar -xzf $(BACKUP_FILE)
	@echo "Restore completed"

# =============================================================================
# Information Commands
# =============================================================================

.PHONY: info
info: ## Show project information
	@echo "Resume/CV AI Project Information"
	@echo "================================"
	@echo "Project: $(PROJECT_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Python: $(PYTHON_VERSION)"
	@echo "Docker Image: $(DOCKER_IMAGE):$(DOCKER_TAG)"
	@echo "Application URL: http://$(APP_HOST):$(APP_PORT)"
	@echo ""

.PHONY: version
version: ## Show version information
	@echo "$(VERSION)"

# =============================================================================
# Dependencies
# =============================================================================

# Ensure directories exist before running commands
$(LOGS_DIR) $(BUILD_DIR) $(DIST_DIR):
	@mkdir -p $@

# =============================================================================
# Notes
# =============================================================================
#
# 1. Make sure to set environment variables before running commands
# 2. Use 'make help' to see all available commands
# 3. Development setup: make dev-setup
# 4. Production deployment: make prod-deploy
# 5. Run tests: make test
# 6. Code quality: make quality
# 7. Clean up: make clean-all
#
# =============================================================================
