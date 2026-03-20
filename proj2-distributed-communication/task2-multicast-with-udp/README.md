# Task 2: Multicast with UDP

Simulates IP multicast by having multiple sender containers broadcast sensor data to a 
multicast group address (224.1.1.1). Multiple receiver containers join the group 
simultaneously and receive messages from all senders at once, demonstrating how multicast 
differs from unicast — one broadcast reaches many receivers without sending individually 
to each.

## Project Structure
- `multicast_sender.py` - Broadcasts JSON sensor data and binary data to the multicast group
- `multicast_receiver.py` - Joins the multicast group, receives both message types, and leaves after a set duration
- `Dockerfile` - Builds a single image used by all containers (senders + receivers)
- `docker-compose.yml` - Orchestrates 2 sender containers and 2 receiver containers

## Notes
- `224.1.1.1` is a reserved multicast IP address. Hardcoded because all senders and 
  receivers must agree on the same "channel" to communicate
- Both sender containers are built from the same image. `SENSOR_TYPE` environment variable 
  set in docker-compose.yml distinguishes them at runtime (temp vs humidity)
- Receivers support `--duration` as a command line argument or `DURATION` as an environment 
  variable. Priority order: `DURATION` env var -> `--duration` flag -> default of 60 seconds
- Dependencies (tcpdump) are installed directly in the Dockerfile via `RUN apt-get install` 
  so no manual installation is needed after build
- Unlike Task 1 (TCP), UDP multicast does not guarantee delivery. Packets may be dropped 
  under network congestion. This is observable via tcpdump by comparing sent vs received counts.

## How to Run

Make sure you are in the `task2-multicast-with-udp/` directory before running any commands:
```bash
cd proj2-distributed-communication/task2-multicast-with-udp
```

**Start all containers:**
```bash
docker-compose up --build
```

**Capture UDP multicast traffic with tcpdump (open a second terminal while containers are running):**
```bash
docker exec -it task2-multicast-with-udp-receiver1-1 tcpdump -i eth0 udp port 5007
```

**Check logs after containers stop:**
```bash
docker logs task2-multicast-with-udp-sender1-1
docker logs task2-multicast-with-udp-sender2-1
docker logs task2-multicast-with-udp-receiver1-1
docker logs task2-multicast-with-udp-receiver2-1
```

**Run receiver manually with --duration flag:**
```bash
docker-compose run receiver1 python -u multicast_receiver.py --duration 45
```

**Stop and remove containers:**
```bash
docker-compose down
```