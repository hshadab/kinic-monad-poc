# Multi-stage build for Kinic Memory Agent on Monad with Python Bindings
# Stage 1: Build kinic-py Python bindings (Rust + Python)
FROM python:3.11-slim as builder

# Install Rust and build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    pkg-config \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /build

# Clone kinic-cli from POC branch
RUN git clone -b poc https://github.com/ICME-Lab/kinic-cli.git
WORKDIR /build/kinic-cli

# Install maturin for building Python bindings
RUN pip install --no-cache-dir maturin setuptools-rust setuptools wheel

# Build kinic-py Python package (PyO3 bindings)
RUN cd /build/kinic-cli && \
    pip install setuptools-rust && \
    pip install -e .

# Stage 2: Build Next.js frontend
FROM node:18-slim as frontend-builder

WORKDIR /frontend

# Copy frontend package files and install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy all frontend source files
COPY frontend/. ./

# Set API URL for production build (same domain for API calls)
ENV NEXT_PUBLIC_API_URL=''

RUN npm run build

# Stage 3: Runtime environment
FROM python:3.11-slim

# Set UTF-8 encoding for Python to handle Unicode characters in logs
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy kinic-cli source for editable install
COPY --from=builder /build/kinic-cli /app/kinic-cli

# Copy Next.js built frontend from frontend-builder
COPY --from=frontend-builder /frontend/out /app/frontend/out

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install kinic-py from the copied source
RUN pip install setuptools-rust && \
    cd /app/kinic-cli && \
    pip install -e .

# Copy application code
COPY src/ ./src/
COPY contracts/ ./contracts/

# Create directory for IC identities
RUN mkdir -p /root/.config/dfx/identity/default

# Create startup script to handle IC identity from environment
RUN echo '#!/bin/bash\n\
# Force UTF-8 encoding\n\
export PYTHONIOENCODING=utf-8\n\
export LANG=C.UTF-8\n\
export LC_ALL=C.UTF-8\n\
\n\
# Write IC identity PEM from environment variable if provided\n\
if [ ! -z "$IC_IDENTITY_PEM" ]; then\n\
    echo "Writing IC identity from environment variable..."\n\
    printf "%s\\n" "$IC_IDENTITY_PEM" > /root/.config/dfx/identity/default/identity.pem\n\
    chmod 600 /root/.config/dfx/identity/default/identity.pem\n\
    echo "IC identity file created:"\n\
    ls -la /root/.config/dfx/identity/default/identity.pem\n\
    echo "IC identity configured successfully"\n\
else\n\
    echo "WARNING: IC_IDENTITY_PEM not set - Kinic functionality will be limited"\n\
fi\n\
\n\
# Verify kinic_py is installed\n\
python3 -c "import kinic_py; print(\"kinic_py version:\", kinic_py.__version__)" || echo "WARNING: kinic_py not installed"\n\
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
