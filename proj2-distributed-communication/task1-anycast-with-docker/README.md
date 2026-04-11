# Task 1: Anycast with Docker (TCP)

Simulates Anycast routing by spinning up 3 server containers that all listen on port 5000. 
A client container connects to each server and receives a unique response, demonstrating 
how Anycast routes a client to one of many available servers.

## Project Structure
- `server.py` - TCP server that reads its identity from the SERVER_ID environment variable
- `client.py` - TCP client that connects to all 3 servers and prints their responses
- `Dockerfile` - Builds a single image used by all 4 containers (servers + client)
- `docker-compose.yml` - Orchestrates 3 server containers and 1 client container

## Notes
- Dependencies (tcpdump) are installed directly in the Dockerfile via `RUN apt-get install` 
  so no manual installation is needed after the containers are built
- All 3 server containers are built from the same image. `SERVER_ID` environment variable 
  set in docker-compose.yml is what distinguishes each server's identity at runtime
- The client container overrides the default CMD from the Dockerfile to run client.py 
  instead of server.py

## How to Run

Make sure you are in the `task1-anycast-with-docker/` directory before running any commands.
```bash
cd proj2-distributed-communication/task1-anycast-with-docker
```

**Start all containers:**
```bash
docker-compose up --build
```

**Check server logs:**
```bash
docker logs task1-anycast-with-docker-server1-1
docker logs task1-anycast-with-docker-server2-1
docker logs task1-anycast-with-docker-server3-1
```

**Capture TCP traffic with tcpdump (open a second terminal while servers are running):**
```bash
docker exec -it task1-anycast-with-docker-server1-1 tcpdump -i eth0 port 5000
```

**Trigger the client manually (while servers are running):**
```bash
docker-compose run client
```

**Stop and remove containers:**
```bash
docker-compose down
```