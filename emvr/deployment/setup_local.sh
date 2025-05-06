#!/bin/bash
set -e

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Enhanced Memory-Vector RAG - Local Setup Script${NC}"
echo -e "${YELLOW}=====================================================${NC}"

# Check for Docker and Docker Compose
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose are installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file. Please edit it with your API keys and settings.${NC}"
    echo -e "${YELLOW}Press any key to open the .env file for editing, or Ctrl+C to exit...${NC}"
    read -n 1 -s
    ${EDITOR:-nano} .env
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p ./monitoring/prometheus ./monitoring/grafana/provisioning/{datasources,dashboards}
echo -e "${GREEN}✓ Created monitoring directories${NC}"

# Pull Docker images
echo -e "${YELLOW}Pulling Docker images (this may take a while)...${NC}"
docker compose pull

echo -e "${GREEN}✓ Setup complete!${NC}"
echo -e "${YELLOW}You can now start the system with:${NC}"
echo -e "${BLUE}docker compose up -d${NC}"
echo -e "${YELLOW}Access the UI at:${NC} http://localhost:8501"
echo -e "${YELLOW}Access the MCP server at:${NC} http://localhost:8000"
echo -e "${YELLOW}Access Grafana at:${NC} http://localhost:3000 (admin/admin)"