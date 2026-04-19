FROM python:3.11-slim

# Install system dependencies for spatial libraries
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Ensure binaries are in path
ENV PATH="/root/.local/bin:$PATH"

# Copy requirements first (this allows Docker to cache this layer)
COPY requirements.txt .

# Install all dependencies at once
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your files
COPY . .

EXPOSE 2718

CMD ["python", "-m", "marimo", "edit", "--host", "0.0.0.0", "--port", "2718", "brooklyn_gentrification.py"]