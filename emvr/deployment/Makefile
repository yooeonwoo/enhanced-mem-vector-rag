.PHONY: setup build up down logs backup restore clean

# Variables
COMPOSE = docker compose
BACKUP_DIR = ./backups
ENV_FILE = .env

setup:
	@echo "Setting up Enhanced Memory-Vector RAG..."
	@./setup_local.sh

build:
	@echo "Building Docker containers..."
	@$(COMPOSE) build

up:
	@echo "Starting all services..."
	@$(COMPOSE) up -d

down:
	@echo "Stopping all services..."
	@$(COMPOSE) down

logs:
	@echo "Viewing logs (press Ctrl+C to stop)..."
	@$(COMPOSE) logs -f

backup:
	@echo "Creating backup..."
	@./scripts/backup.sh

restore:
	@if [ -z "$(file)" ]; then \
		echo "Error: Backup file not specified. Use make restore file=<backup_file>"; \
		exit 1; \
	fi
	@echo "Restoring from $(file)..."
	@./scripts/restore.sh $(file)

token:
	@if [ -z "$(user)" ]; then \
		echo "Error: User not specified. Use make token user=<user_id>"; \
		exit 1; \
	fi
	@echo "Generating token for $(user)..."
	@python3 ./scripts/generate_token.py $(user)

clean:
	@echo "Cleaning up..."
	@$(COMPOSE) down -v
	@echo "Removing Docker images..."
	@docker rmi -f $(shell docker images --filter "reference=enhanced-mem-vector-rag*" -q)
	@echo "Cleanup complete"

help:
	@echo "Enhanced Memory-Vector RAG Deployment Help"
	@echo "-------------------------------------"
	@echo "make setup     - Run setup script"
	@echo "make build     - Build Docker containers"
	@echo "make up        - Start all services"
	@echo "make down      - Stop all services"
	@echo "make logs      - View logs (press Ctrl+C to stop)"
	@echo "make backup    - Create backup of all data"
	@echo "make restore file=<backup_file> - Restore from backup"
	@echo "make token user=<user_id>       - Generate token for a user"
	@echo "make clean     - Stop services and clean up volumes/images"
	@echo "make help      - Show this help message"