#!/bin/bash

# EMVR Setup Script

# Set output colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Enhanced Memory-Vector RAG Setup Script${NC}"
echo -e "${BLUE}======================================${NC}"

# Check for Python 3.11+
echo -e "\n${YELLOW}Checking Python version...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 11 ]; then
        echo -e "${GREEN}Found Python $PYTHON_VERSION ✓${NC}"
        PYTHON_CMD=python3
    else
        echo -e "${RED}Error: Python 3.11+ required, found $PYTHON_VERSION${NC}"
        echo -e "${YELLOW}Please install Python 3.11 or later and try again.${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: Python 3.11+ not found${NC}"
    echo -e "${YELLOW}Please install Python 3.11 or later and try again.${NC}"
    exit 1
fi

# Check for Docker
echo -e "\n${YELLOW}Checking for Docker...${NC}"
if command -v docker &>/dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    echo -e "${GREEN}Found Docker $DOCKER_VERSION ✓${NC}"
else
    echo -e "${RED}Error: Docker not found${NC}"
    echo -e "${YELLOW}Please install Docker and try again:${NC}"
    echo -e "${YELLOW}https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

# Check for Docker Compose
echo -e "\n${YELLOW}Checking for Docker Compose...${NC}"
if docker compose version &>/dev/null; then
    COMPOSE_VERSION=$(docker compose version | awk '{print $4}')
    echo -e "${GREEN}Found Docker Compose $COMPOSE_VERSION ✓${NC}"
else
    echo -e "${RED}Error: Docker Compose not found${NC}"
    echo -e "${YELLOW}Please install Docker Compose and try again:${NC}"
    echo -e "${YELLOW}https://docs.docker.com/compose/install/${NC}"
    exit 1
fi

# Check if uv is installed, otherwise install it
echo -e "\n${YELLOW}Checking for uv package manager...${NC}"
if command -v uv &>/dev/null; then
    UV_VERSION=$(uv --version | head -n 1)
    echo -e "${GREEN}Found uv $UV_VERSION ✓${NC}"
else
    echo -e "${YELLOW}Installing uv package manager...${NC}"
    $PYTHON_CMD -m pip install uv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Installed uv successfully ✓${NC}"
    else
        echo -e "${RED}Failed to install uv${NC}"
        echo -e "${YELLOW}Consider installing it manually: pip install uv${NC}"
        exit 1
    fi
fi

# Setup virtual environment
echo -e "\n${YELLOW}Setting up virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    uv venv .venv
    echo -e "${GREEN}Created virtual environment ✓${NC}"
else
    echo -e "${GREEN}Virtual environment already exists ✓${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi
echo -e "${GREEN}Virtual environment activated ✓${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
uv pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Installed dependencies successfully ✓${NC}"
else
    echo -e "${RED}Error installing dependencies${NC}"
    exit 1
fi

# Setup environment file
echo -e "\n${YELLOW}Setting up environment file...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}Created .env file ✓${NC}"
    echo -e "${YELLOW}Please edit the .env file to add your API keys and configuration.${NC}"
else
    echo -e "${GREEN}.env file already exists ✓${NC}"
    echo -e "${YELLOW}Make sure your .env file has the necessary API keys and configuration.${NC}"
fi

# Start Docker containers
echo -e "\n${YELLOW}Would you like to start the Docker containers now? (y/n)${NC}"
read -p "" start_docker

if [[ $start_docker == "y" || $start_docker == "Y" ]]; then
    echo -e "\n${YELLOW}Starting Docker containers...${NC}"
    cd emvr/deployment
    docker compose up -d
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Started Docker containers successfully ✓${NC}"
    else
        echo -e "${RED}Error starting Docker containers${NC}"
        exit 1
    fi
fi

# Final message
echo -e "\n${GREEN}======================================${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}======================================${NC}"
echo -e "\n${YELLOW}To get started, follow these steps:${NC}"
echo -e "1. Edit the ${BLUE}.env${NC} file to add your API keys"
echo -e "2. Activate the virtual environment: ${BLUE}source .venv/bin/activate${NC}"
echo -e "3. Run the MCP server: ${BLUE}uv run -m emvr.mcp_server${NC}"
echo -e "4. In another terminal, run the UI: ${BLUE}uv run -m emvr.ui.app${NC}"
echo -e "\n${YELLOW}Documentation:${NC}"
echo -e "- Project overview: ${BLUE}README.md${NC}"
echo -e "- Development with Claude Code: ${BLUE}CLAUDE.md${NC}"
echo -e "- Contribution guidelines: ${BLUE}CONTRIBUTING.md${NC}"
echo -e "\n${GREEN}Happy coding!${NC}"