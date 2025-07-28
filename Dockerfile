# Use official slim Python base image with amd64 platform
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application code
COPY main.py .

# Create input/output directories (useful if running manually)
RUN mkdir -p /app/input /app/output

# Command to run the processing script
CMD ["python", "main.py"]