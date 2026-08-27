FROM python:3.10-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python output buffering
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# System dependencies required by Presidio / spaCy
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install the spaCy English model required by Presidio
RUN python -m spacy download en_core_web_sm

# Copy application source
COPY app ./app

# Copy policy and other required project data
COPY data ./data

# FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
