# Multi-Container Server-Client Application

TCP echo server with multiple client containers demonstrating Docker networking.

## Architecture

- **Server:** Python TCP server listening on port 5000
- **Client1 & Client2:** Python clients that connect to server
- **Network:** Docker bridge network enabling container-to-container communication

## Files

- `server.py` - TCP echo server implementation
- `client.py` - Client that sends messages to server
- `Dockerfile` - Image definition for both server and clients
- `docker-compose.yml` - Multi-container orchestration

## How to Run
```bash
# Build and start all containers
docker-compose up
```
Press `Ctrl+C` to stop when finished.

## Advanced Options
```bash
# Run in background
docker-compose up -d

# View logs later
docker-compose logs

# Stop and remove containers
docker-compose down
```

## Expected Output
```
server  | Server listening on 0.0.0.0:5000
server  | Connection from ('172.19.0.4', 49810)
server  | Received: Hello from our group!
client1  | Sent: Hello from our group!
client1  | Received: Echo: Hello from our group!
server   | Connection from ('172.19.0.3', 46528)
client2  | Sent: Hello from our group!
server   | Received: Hello from our group!
client2  | Received: Echo: Hello from our group!
client2 exited with code 0
client1 exited with code 0
```

## How It Works

1. **Docker Compose** creates isolated network `app-network`
2. **Server container** starts, binds to port 5000
3. **Client containers** wait for server (`depends_on`)
4. **Clients connect** to server using hostname `server` (Docker DNS)
5. **Server echoes** messages back to clients
6. **Clients exit** after receiving response