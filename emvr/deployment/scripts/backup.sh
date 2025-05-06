#!/bin/bash
# Backup script for EMVR components

set -e

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Timestamp for backup files
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups/$TIMESTAMP"

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo -e "${BLUE}Enhanced Memory-Vector RAG - Backup Script${NC}"
echo -e "${YELLOW}=====================================================${NC}"
echo -e "${YELLOW}Creating backup in $BACKUP_DIR${NC}"

# Backup Neo4j
echo -e "${YELLOW}Backing up Neo4j...${NC}"
docker compose exec -T neo4j neo4j-admin dump --database=neo4j --to=/tmp/neo4j_backup.dump
docker compose cp neo4j:/tmp/neo4j_backup.dump "$BACKUP_DIR/neo4j_backup.dump"
echo -e "${GREEN}✓ Neo4j backup completed${NC}"

# Backup Qdrant
echo -e "${YELLOW}Backing up Qdrant storage...${NC}"
docker compose exec -T qdrant tar -czf /tmp/qdrant_backup.tar.gz -C /qdrant storage
docker compose cp qdrant:/tmp/qdrant_backup.tar.gz "$BACKUP_DIR/qdrant_backup.tar.gz"
echo -e "${GREEN}✓ Qdrant backup completed${NC}"

# Backup Supabase PostgreSQL
echo -e "${YELLOW}Backing up Supabase PostgreSQL...${NC}"
docker compose exec -T supabase pg_dump -U postgres postgres > "$BACKUP_DIR/postgres_backup.sql"
echo -e "${GREEN}✓ PostgreSQL backup completed${NC}"

# Backup MCP server models and logs
echo -e "${YELLOW}Backing up MCP server models and logs...${NC}"
docker compose exec -T mcp-server tar -czf /tmp/mcp_models_backup.tar.gz -C /app models
docker compose cp mcp-server:/tmp/mcp_models_backup.tar.gz "$BACKUP_DIR/mcp_models_backup.tar.gz"
docker compose exec -T mcp-server tar -czf /tmp/mcp_logs_backup.tar.gz -C /app logs
docker compose cp mcp-server:/tmp/mcp_logs_backup.tar.gz "$BACKUP_DIR/mcp_logs_backup.tar.gz"
echo -e "${GREEN}✓ MCP server backup completed${NC}"

# Backup UI uploads
echo -e "${YELLOW}Backing up UI uploads...${NC}"
docker compose exec -T chainlit-ui tar -czf /tmp/uploads_backup.tar.gz -C /app uploads
docker compose cp chainlit-ui:/tmp/uploads_backup.tar.gz "$BACKUP_DIR/uploads_backup.tar.gz"
echo -e "${GREEN}✓ UI uploads backup completed${NC}"

# Create backup manifest
echo -e "${YELLOW}Creating backup manifest...${NC}"
cat > "$BACKUP_DIR/manifest.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "components": {
    "neo4j": {
      "file": "neo4j_backup.dump",
      "size": "$(du -h "$BACKUP_DIR/neo4j_backup.dump" | cut -f1)"
    },
    "qdrant": {
      "file": "qdrant_backup.tar.gz",
      "size": "$(du -h "$BACKUP_DIR/qdrant_backup.tar.gz" | cut -f1)"
    },
    "postgres": {
      "file": "postgres_backup.sql",
      "size": "$(du -h "$BACKUP_DIR/postgres_backup.sql" | cut -f1)"
    },
    "mcp_server": {
      "models": "mcp_models_backup.tar.gz",
      "models_size": "$(du -h "$BACKUP_DIR/mcp_models_backup.tar.gz" | cut -f1)",
      "logs": "mcp_logs_backup.tar.gz",
      "logs_size": "$(du -h "$BACKUP_DIR/mcp_logs_backup.tar.gz" | cut -f1)"
    },
    "ui": {
      "uploads": "uploads_backup.tar.gz",
      "uploads_size": "$(du -h "$BACKUP_DIR/uploads_backup.tar.gz" | cut -f1)"
    }
  }
}
EOF
echo -e "${GREEN}✓ Backup manifest created${NC}"

# Create single compressed archive
echo -e "${YELLOW}Creating compressed archive of all backups...${NC}"
tar -czf "./backups/emvr_backup_$TIMESTAMP.tar.gz" -C "./backups" "$TIMESTAMP"
echo -e "${GREEN}✓ Compressed archive created at ./backups/emvr_backup_$TIMESTAMP.tar.gz${NC}"

echo -e "${GREEN}Backup completed successfully!${NC}"
echo -e "${YELLOW}Backup size: $(du -h "./backups/emvr_backup_$TIMESTAMP.tar.gz" | cut -f1)${NC}"