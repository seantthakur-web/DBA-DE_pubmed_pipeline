# ================================
# Stage 1 — Base Python Image
# Streamlit UI for PubMed Pipeline
# ================================
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Work inside /app
WORKDIR /app

# *** CRITICAL FIX ***
# Tells Python where your "ui" folder lives
ENV PYTHONPATH="/app"

# Install OS deps
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy repo-level requirements
COPY requirements.txt /app/requirements.txt

# Install Python deps
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy only the UI folder
COPY ui /app/ui
COPY ui/.streamlit /app/ui/.streamlit

# Streamlit runs on port 8501
EXPOSE 8501

# Entry point for the container
CMD ["streamlit", "run", "ui/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
