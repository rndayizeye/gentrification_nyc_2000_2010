FROM python:3.11-slim

# Install system dependencies for spatial libraries (GDAL, PROJ, GEOS)
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PATH="/root/.local/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 2718

CMD ["python", "-m", "marimo", "edit", "--host", "0.0.0.0", "--port", "2718", "brooklyn_gentrification.py"]