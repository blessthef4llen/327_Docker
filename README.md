# CECS 327 - Project 1: Docker Containers

Group Members:
- Seth Lunas
- Han Htoo Zin
- Christopher Dominguez

## Project Overview

This project demonstrates Docker containerization through:
1. Creating custom docker images
2. Deploying a web server (Nginx)
3. Building a multi-container client-server application

## Repository Structure
```
327_Docker/
    - python_app/   # Task 1: Custom Python Docker image + Nginx web server
    - server_clients/   # Task 2: Multi-container setup (server + clients)
    - README.md     # This file
```

## Prerequisites
- Docker Desktop installed
- At least 4GB RAM
- 20GB free storage

## Quick Start

### Task 1: Python Application
```bash
cd python_app
docker build -t my-python-app .
docker run my-python-app
```

### Task 2: Nginx Web Server
```bash
cd python_app
docker pull nginx:latest
docker run -d -p 8080:80 --name my-nginx nginx:latest
# Visit http://localhost:8080

# With custom page
docker run -d -p 8080:80 -v $(pwd)/index.html:/usr/share/nginx/html/index.html nginx:latest
```

### Task 3: Multi-Contaier Server + Clients
```bash
cd server-clients
docker-compose up
# Server accessible at localhost:5001
```

**Note:** Server runs on port 5001 (host) -> 5000 (container)

## Troubleshooting

**View logs:**
```bash
docker-compose logs
```

**Clean up:**
```bash
docker-compose down
docker container prune
```

## Video Demonstration

https://youtu.be/4jRV7jLdUFs

## Report

See `/docs/CECS 327 - Project 1 Report.pdf` for project report.
