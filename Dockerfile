# Use Python 3.11 as base image (built on top of Debian Linux)
FROM python:3.11

# Set working directory to /app
WORKDIR /app

# Copy application file to working directory
COPY app.py . 

# Run the Python script
CMD ["python3", "app.py"]