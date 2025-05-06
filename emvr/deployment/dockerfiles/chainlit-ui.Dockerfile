FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for package management
RUN pip install --no-cache-dir uv

# Copy dependency files 
COPY pyproject.toml requirements.txt* ./

# Install dependencies in a virtual environment
RUN uv pip install --no-cache-dir -r requirements.txt

# Second stage: runtime
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment
COPY --from=builder /app /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy application code and Chainlit configuration
COPY emvr /app/emvr
COPY chainlit.md /app/
COPY chainlit.yaml /app/

# Create necessary directories
RUN mkdir -p /app/logs /app/uploads

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m emvruser
RUN chown -R emvruser:emvruser /app
USER emvruser

# Set healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/ || exit 1

# Start the Chainlit UI
CMD ["chainlit", "run", "emvr/ui/app.py", "--port", "8501", "--host", "0.0.0.0"]

EXPOSE 8501