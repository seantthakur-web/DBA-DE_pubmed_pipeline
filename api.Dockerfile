FROM python:3.12-slim

WORKDIR /app

# Install OS dependencies (psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY pubmed_pipeline /app/pubmed_pipeline

# Copy startup script
COPY startup_api.sh /app/startup_api.sh
RUN chmod +x /app/startup_api.sh

# Expose FastAPI port
EXPOSE 8000

# Start the app
CMD ["bash", "/app/startup_api.sh"]
