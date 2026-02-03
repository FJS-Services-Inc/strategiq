# Pygentic-AI Justfile
# Task automation for Docker, development, and deployment workflows

# Default recipe - show available commands
default:
    @just --list

# Variables with sensible defaults
IMAGE_NAME := "s3docker.francissecada.com/pygentic_ai"
COMPOSE_FILE := "compose.yaml"

# ============================================
# Docker Build Commands
# ============================================

# Build Docker image with optional tag (default: dev-latest)
build tag="dev-latest":
    @echo "Building Docker image: {{IMAGE_NAME}}:{{tag}}"
    docker build -t {{IMAGE_NAME}}:{{tag}} .

# Build image with custom branch tag
build-branch branch="dev_deploy":
    @echo "Building image with branch tag: {{branch}}"
    docker build -t {{IMAGE_NAME}}:{{branch}}-latest .

# Build and push image
build-push tag="dev-latest":
    @echo "Building and pushing: {{IMAGE_NAME}}:{{tag}}"
    docker build -t {{IMAGE_NAME}}:{{tag}} --push .

# ============================================
# Docker Compose Commands
# ============================================

# Start all services
up *args="":
    docker-compose -f {{COMPOSE_FILE}} up {{args}}

# Start services in detached mode
up-d:
    docker-compose -f {{COMPOSE_FILE}} up -d

# Stop all services
down:
    docker-compose -f {{COMPOSE_FILE}} down

# Restart services
restart:
    docker-compose -f {{COMPOSE_FILE}} restart

# View logs (optional service name and follow flag)
logs service="" follow="":
    #!/usr/bin/env bash
    if [ -n "{{service}}" ]; then
        docker-compose -f {{COMPOSE_FILE}} logs {{follow}} {{service}}
    else
        docker-compose -f {{COMPOSE_FILE}} logs {{follow}}
    fi

# Follow logs for all services
logs-f:
    docker-compose -f {{COMPOSE_FILE}} logs -f

# Follow logs for web service
logs-web:
    docker-compose -f {{COMPOSE_FILE}} logs -f web

# Follow logs for celery service
logs-celery:
    docker-compose -f {{COMPOSE_FILE}} logs -f celery_service

# ============================================
# Development Commands
# ============================================

# Install Python dependencies with uv
install:
    uv sync --all-extras --dev

# Run FastAPI development server
dev:
    uv run python src/app.py

# Run Celery worker
celery:
    uv run python src/cworker.py

# Compile SCSS to CSS
scss:
    cd src/frontend && npm run build:css

# Watch SCSS files and recompile on changes
scss-watch:
    cd src/frontend && npm run watch:css

# Install frontend dependencies
npm-install:
    cd src/frontend && npm install

# ============================================
# Testing & Quality Commands
# ============================================

# Run all tests
test:
    uv run pytest tests/ -v

# Run tests with coverage
test-cov:
    uv run pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run linting checks
lint:
    uv run ruff check src/

# Run formatting
format:
    uv run black src/
    uv run ruff check --fix src/

# Run security checks
security:
    uv run bandit -r src/

# ============================================
# Health & Status Commands
# ============================================

# Check if services are healthy
health:
    @echo "Checking web service health..."
    @curl -f -H "Host: pygenticai.francissecada.com" http://localhost:5051/ || echo "Web service is not responding"

# Check Docker container status
ps:
    docker-compose -f {{COMPOSE_FILE}} ps

# Show container resource usage
stats:
    docker stats --no-stream

# ============================================
# Database Commands
# ============================================

# Run database migrations (placeholder - add your migration tool)
migrate:
    @echo "Running migrations..."
    # uv run alembic upgrade head

# Create new migration
migration name:
    @echo "Creating migration: {{name}}"
    # uv run alembic revision --autogenerate -m "{{name}}"

# Reset database (WARNING: destructive)
db-reset:
    @echo "WARNING: This will delete all data!"
    @read -p "Are you sure? (y/N) " -n 1 -r
    @echo
    # Add your reset commands here

# ============================================
# Cleanup Commands
# ============================================

# Stop and remove all containers, networks
clean:
    docker-compose -f {{COMPOSE_FILE}} down -v

# Remove all Pygentic-AI Docker images
clean-images:
    docker images {{IMAGE_NAME}} -q | xargs -r docker rmi -f

# Full cleanup - containers, images, volumes
clean-all: clean clean-images
    @echo "Cleaned up all Pygentic-AI Docker resources"

# Remove unused Docker resources
prune:
    docker system prune -f

# ============================================
# Deployment Commands
# ============================================

# Deploy with specific image tag
deploy tag="main-latest":
    @echo "Deploying with IMAGE_TAG={{tag}}"
    IMAGE_TAG={{tag}} docker-compose -f {{COMPOSE_FILE}} up -d

# Pull latest images
pull tag="main-latest":
    docker pull {{IMAGE_NAME}}:{{tag}}

# Deploy latest from main branch
deploy-main: (pull "main-latest")
    IMAGE_TAG=main-latest docker-compose -f {{COMPOSE_FILE}} up -d

# Deploy from dev branch
deploy-dev: (pull "dev_deploy-latest")
    IMAGE_TAG=dev_deploy-latest docker-compose -f {{COMPOSE_FILE}} up -d

# ============================================
# Environment Setup
# ============================================

# Create .env from template
init-env:
    @if [ ! -f .env ]; then \
        cp .env.example .env; \
        echo "Created .env from template. Please update with your credentials."; \
    else \
        echo ".env already exists. Skipping."; \
    fi

# Validate environment variables
check-env:
    @echo "Checking required environment variables..."
    @grep -v '^#' .env.example | grep '=' | cut -d'=' -f1 | while read var; do \
        if ! grep -q "^$var=" .env 2>/dev/null; then \
            echo "Missing: $var"; \
        fi; \
    done

# ============================================
# Development Workflow
# ============================================

# Full development setup
setup: init-env npm-install install scss
    @echo "✅ Development environment ready!"
    @echo "Run 'just dev' to start the development server"

# Start complete development environment
dev-full: scss-watch dev

# Rebuild and restart services
rebuild: build up-d
    @echo "Services rebuilt and restarted"

# ============================================
# CI/CD Helpers
# ============================================

# Simulate CI build
ci-build:
    @echo "Simulating CI build process..."
    just build dev_deploy-$(date +%Y-%m-%d)

# Run all quality checks (for pre-commit)
check: lint test
    @echo "✅ All checks passed!"

# ============================================
# Information Commands
# ============================================

# Show environment information
info:
    @echo "Project: Pygentic-AI"
    @echo "Image: {{IMAGE_NAME}}"
    @echo "Compose: {{COMPOSE_FILE}}"
    @echo ""
    @echo "Python version:"
    @uv run python --version
    @echo ""
    @echo "Docker version:"
    @docker --version
    @echo ""
    @echo "Docker Compose version:"
    @docker-compose --version

# Show current configuration
config:
    docker-compose -f {{COMPOSE_FILE}} config

# ============================================
# Claude AI Assistance
# ============================================

# Start Claude with full project context and multi-agent orchestration
start-claude *args="":
    @echo "🤖 Starting Claude with Pygentic-AI context..."
    @echo "📋 System Prompt: .claude/system-prompt.md (Multi-agent orchestration)"
    @echo "📖 Project Context: CLAUDE.md (Initialization guide)"
    @echo ""
    @if [ ! -f .claude/system-prompt.md ]; then \
        echo "❌ Error: .claude/system-prompt.md not found"; \
        echo "Run: git pull origin dev_deploy"; \
        exit 1; \
    fi
    @if [ ! -f CLAUDE.md ]; then \
        echo "❌ Error: CLAUDE.md not found"; \
        echo "Run: git pull origin dev_deploy"; \
        exit 1; \
    fi
    @echo "✅ All context files found"
    @echo ""
    @echo "Claude will load with:"
    @echo "  • Multi-agent orchestration (🏗️ Architect, 🎨 Frontend, ⚙️ Backend, 🔒 Security, 🚀 DevOps)"
    @echo "  • MCP server routing (Sequential, Context7, Magic, Playwright, Morphllm, Serena)"
    @echo "  • Project architecture and workflows"
    @echo ""
    @echo "🚀 Launching Claude Code CLI..."
    @echo "   System Prompt: .claude/system-prompt.md"
    @echo "   Use /init in Claude to load CLAUDE.md context"
    @echo ""
    claude --system-prompt-file .claude/system-prompt.md {{args}}
