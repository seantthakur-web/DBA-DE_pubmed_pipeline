# 1. Base Image
FROM python:3.12-slim

# 2. Working Directory
WORKDIR /app

# 3. Add Python path so 'ui' imports work
ENV PYTHONPATH="/app"

# 4. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy only requirements first (optimizes Docker build cache)
COPY requirements.txt /app/requirements.txt

# 6. Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# 7. Copy entire project
COPY . /app

# 8. Expose Streamlit port
EXPOSE 8501

# 9. Start Streamlit
CMD ["streamlit", "run", "ui/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

