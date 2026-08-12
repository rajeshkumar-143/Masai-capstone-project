
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by chromadb
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Assuming requirements.txt will contain: fastapi, uvicorn, nest_asyncio, langgraph, chromadb, sentence-transformers, pydantic, requests
# For simplicity, we'll install them directly here if no requirements.txt is provided yet.
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    nest_asyncio \
    langgraph \
    chromadb \
    sentence-transformers \
    pydantic \
    requests \
    "pydantic_core<2.13.0" # Pinning for compatibility with older pydantic versions if needed

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the uvicorn server
# Assuming the FastAPI app instance is named 'app_fastapi' in a file named 'main.py'
# For this notebook, the app is defined directly, so we need to create a main.py
CMD sh -c "python -c \"from main import app_fastapi; import uvicorn; uvicorn.run(app_fastapi, host='0.0.0.0', port=8000)\""
