FROM python:3.11

WORKDIR /app

COPY server.py .
COPY client.py .

EXPOSE 5000

# Install tcpdump for capturing network traffic (required for deliverables)
RUN apt-get update && apt-get install -y tcpdump 

CMD ["python", "-u", "server.py"]