# Python Application & Nginx Web Server

Simple Python application containerization and Nginx web server deployment.

## Files

- `app.py` - Simple Python script
- `Dockerfile` - Image definition for Python app
- `index.html` - Custom HTML page for Nginx

## Task 1: Python Application

Build and run containerized Python app:
```bash
# Build image
docker build -t my-python-app .

# Run container
docker run my-python-app
```

**Expected output:**
```
Hello, Docker! This is my first containerized app.
```

## Task 2: Nginx Web Server

### Default Nginx
```bash
# Pull image
docker pull nginx:latest

# Run container
docker run -d -p 8080:80 --name my-nginx nginx:latest
# Visit http://localhost:8080
```

### Custom HTML Page
```bash
# Run with volume mount
docker run -d -p 8080:80 -v $(pwd)/index.html:/usr/share/nginx/html/index.html nginx:latest
# Visit http://localhost:8080
```

## Dockerfile Explanation
```dockerfile
FROM python:3.11    # Base image with Python pre-installed
WORKDIR /app    # Set working directory
COPY app.py     # Copy application file
CMD ["python", "app.py"]    # Run script
```

## Cleanup
```bash
# Stop and remove containers
docker stop my-nginx
docker rm my-nginx

# Remove images
docker rmi my-python-app nginx:latest
```

