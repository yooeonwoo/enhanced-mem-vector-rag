#!/bin/bash
# Restore script for EMVR components

set -e

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

if [ $# -ne 1 ]; then
    echo -e "${RED}Error: Backup archive path is required${NC}"
    echo -e "Usage: $0 <backup_archive_path>"
    exit 1
fi

BACKUP_ARCHIVE=$1

if [ ! -f "$BACKUP_ARCHIVE" ]; then
    echo -e "${RED}Error: Backup archive not found: $BACKUP_ARCHIVE${NC}"
    exit 1
fi

TEMP_DIR=$(mktemp -d)
RESTORE_DIR="$TEMP_DIR/restore"

echo -e "${BLUE}Enhanced Memory-Vector RAG - Restore Script${NC}"
echo -e "${YELLOW}=====================================================${NC}"
echo -e "${YELLOW}Extracting backup archive...${NC}"

# Extract the backup archive
mkdir -p "$RESTORE_DIR"
tar -xzf "$BACKUP_ARCHIVE" -C "$RESTORE_DIR"

# Find the timestamp directory
TIMESTAMP_DIR=$(find "$RESTORE_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)

if [ -z "$TIMESTAMP_DIR" ]; then
    echo -e "${RED}Error: Invalid backup archive structure${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}✓ Backup archive extracted${NC}"

# Verify the backup manifest
if [ ! -f "$TIMESTAMP_DIR/manifest.json" ]; then
    echo -e "${RED}Error: Backup manifest not found${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${BLUE}Restore will include the following components:${NC}"
cat "$TIMESTAMP_DIR/manifest.json"
echo

# Confirm restoration
echo -e "${YELLOW}WARNING: This will override current data. Make sure the system is stopped before proceeding.${NC}"
read -p "Are you sure you want to proceed with restoration? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Restore cancelled.${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${YELLOW}Checking if Docker Compose services are running...${NC}"
if docker compose ps | grep -q Up; then
    echo -e "${RED}Error: Some services are still running. Please stop them first:${NC}"
    echo -e "${BLUE}docker compose down${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}✓ All services are stopped${NC}"

# Start the databases for restoration
echo -e "${YELLOW}Starting databases for restoration...${NC}"
docker compose up -d neo4j qdrant supabase
echo -e "${GREEN}✓ Databases started${NC}"

# Give the databases time to initialize
echo -e "${YELLOW}Waiting for databases to initialize...${NC}"
sleep 15

# Restore Neo4j
echo -e "${YELLOW}Restoring Neo4j...${NC}"
docker compose cp "$TIMESTAMP_DIR/neo4j_backup.dump" neo4j:/tmp/neo4j_backup.dump
docker compose exec -T neo4j neo4j-admin load --database=neo4j --from=/tmp/neo4j_backup.dump --force
echo -e "${GREEN}✓ Neo4j restored${NC}"

# Restore Qdrant
echo -e "${YELLOW}Restoring Qdrant...${NC}"
docker compose cp "$TIMESTAMP_DIR/qdrant_backup.tar.gz" qdrant:/tmp/qdrant_backup.tar.gz
docker compose exec -T qdrant sh -c "rm -rf /qdrant/storage/*"
docker compose exec -T qdrant tar -xzf /tmp/qdrant_backup.tar.gz -C /qdrant
echo -e "${GREEN}✓ Qdrant restored${NC}"

# Restore PostgreSQL
echo -e "${YELLOW}Restoring PostgreSQL...${NC}"
cat "$TIMESTAMP_DIR/postgres_backup.sql" | docker compose exec -T supabase psql -U postgres postgres
echo -e "${GREEN}✓ PostgreSQL restored${NC}"

# Stop the databases
echo -e "${YELLOW}Stopping databases...${NC}"
docker compose down
echo -e "${GREEN}✓ Databases stopped${NC}"

# Create directories for other components
echo -e "${YELLOW}Preparing directories for other components...${NC}"
mkdir -p ./volumes/mcp/models ./volumes/mcp/logs ./volumes/ui/uploads
echo -e "${GREEN}✓ Directories prepared${NC}"

# Extract other component data to bind mount directories
echo -e "${YELLOW}Extracting MCP server and UI data...${NC}"
tar -xzf "$TIMESTAMP_DIR/mcp_models_backup.tar.gz" -C ./volumes/mcp/
tar -xzf "$TIMESTAMP_DIR/mcp_logs_backup.tar.gz" -C ./volumes/mcp/
tar -xzf "$TIMESTAMP_DIR/uploads_backup.tar.gz" -C ./volumes/ui/
echo -e "${GREEN}✓ Component data extracted${NC}"

# Clean up
echo -e "${YELLOW}Cleaning up temporary files...${NC}"
rm -rf "$TEMP_DIR"
echo -e "${GREEN}✓ Cleanup completed${NC}"

echo -e "${GREEN}Restore completed successfully!${NC}"
echo -e "${YELLOW}You can now start the system with:${NC}"
echo -e "${BLUE}docker compose up -d${NC}"