# Dockerfile for Flask-based Quantum RAG App

# Use Python base image (or switch to CUDA base for GPU)
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all source code into the container
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Dockerfile
COPY chroma_bge_768/ chroma_bge_768/

# Start the Flask app
CMD ["python", "app.py"]