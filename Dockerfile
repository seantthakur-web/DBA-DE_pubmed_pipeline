# 1. Base Image
FROM python:3.12-slim

# 2. Working Directory
WORKDIR /app

# 3. Install system dependencies (for psycopg, pgvector, etc.)
RUN apt-get update && apt-get install -y build-essential

# 4. Copy project
COPY . /app

# 5. Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Expose Streamlit port
EXPOSE 8501

# 7. Start Streamlit
CMD ["streamlit", "run", "ui/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
