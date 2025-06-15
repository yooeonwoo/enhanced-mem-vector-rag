FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY emvr /app/emvr

# Create necessary directories
RUN mkdir -p /app/logs /app/models /app/uploads

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m emvruser && \
    chown -R emvruser:emvruser /app
USER emvruser

# Set healthcheck - disable for debugging
# HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1

# Start the MCP Server
CMD ["python", "-m", "emvr.mcp_server.server"]

EXPOSE 8000