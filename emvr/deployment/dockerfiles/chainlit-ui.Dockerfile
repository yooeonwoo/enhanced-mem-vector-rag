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

# Copy application code and Chainlit configuration
COPY emvr /app/emvr
COPY chainlit.md /app/ 2>/dev/null || echo "chainlit.md not found, skipping"
COPY chainlit.yaml /app/ 2>/dev/null || echo "chainlit.yaml not found, skipping"

# Create necessary directories
RUN mkdir -p /app/logs /app/uploads

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m emvruser && \
    chown -R emvruser:emvruser /app
USER emvruser

# Set healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/ || exit 1

# Start the Chainlit UI
CMD ["chainlit", "run", "emvr/ui/app.py", "--port", "8501", "--host", "0.0.0.0"]

EXPOSE 8501