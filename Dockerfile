# Pure Python Dockerfile for Kinic Memory Agent on Monad
# No Rust needed - uses ic-py for Internet Computer interaction

# Stage 1: Build Next.js frontend
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

# Stage 2: Runtime environment (pure Python)
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

# Copy Next.js built frontend from frontend-builder
COPY --from=frontend-builder /frontend/out /app/frontend/out

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
# Force UTF-8 encoding\n\
export PYTHONIOENCODING=utf-8\n\
export LANG=C.UTF-8\n\
export LC_ALL=C.UTF-8\n\
\n\
# Write IC identity PEM from environment variable if provided\n\
if [ ! -z "$IC_IDENTITY_PEM" ]; then\n\
    echo "IC identity PEM provided in environment (pure Python client)"\n\
    echo "✅ Pure Python ic-py client will use IC_IDENTITY_PEM directly"\n\
else\n\
    echo "WARNING: IC_IDENTITY_PEM not set - Kinic functionality will be limited"\n\
fi\n\
\n\
# Verify ic-py is installed\n\
python3 -c "from ic.client import Client; print(\"✅ ic-py installed successfully\")" || echo "WARNING: ic-py not installed"\n\
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
