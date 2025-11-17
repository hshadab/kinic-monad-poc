# Multi-stage build for Kinic Memory Agent on Monad
# Stage 1: Build kinic-cli (Rust)
FROM rustlang/rust:nightly-slim as builder

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
    curl \
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

# Create startup script to handle IC identity from environment
RUN echo '#!/bin/bash\n\
# Write IC identity PEM from environment variable if provided\n\
if [ ! -z "$IC_IDENTITY_PEM" ]; then\n\
    echo "📝 Writing IC identity from environment variable..."\n\
    echo "$IC_IDENTITY_PEM" > /root/.config/dfx/identity/default/identity.pem\n\
    chmod 600 /root/.config/dfx/identity/default/identity.pem\n\
    echo "✅ IC identity configured"\n\
else\n\
    echo "⚠️  IC_IDENTITY_PEM not set - Kinic functionality will be limited"\n\
fi\n\
\n\
# Start the application\n\
exec uvicorn src.main:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application via startup script
CMD ["/app/start.sh"]
