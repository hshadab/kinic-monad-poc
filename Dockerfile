# Multi-stage build for Kinic Memory Agent on Monad
# Stage 1: Build kinic-cli (Rust)
FROM rust:1.75-slim as builder

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Clone and build kinic-cli from POC branch
RUN git clone -b poc https://github.com/ICME-Lab/kinic-cli.git
WORKDIR /build/kinic-cli
RUN cargo build --release

# Stage 2: Runtime environment
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy kinic-cli binary from builder
COPY --from=builder /build/kinic-cli/target/release/kinic-cli /app/kinic-cli/target/release/kinic-cli

# Make binary executable
RUN chmod +x /app/kinic-cli/target/release/kinic-cli

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY contracts/ ./contracts/

# Create directory for IC identities
RUN mkdir -p /root/.config/dfx/identity/default

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
