# Use Python 3.11 as base image (Debian + Python pre-installed)
FROM python:3.11

# Set working directory - creates /app inside container, cd into it
WORKDIR /app

# Copy server script to working directory
COPY server.py .

# Tells docker-compose / other devs "this container uses port 5000"
EXPOSE 5000

# Run server when container starts - executes `python server.py`
CMD ["python", "server.py"]