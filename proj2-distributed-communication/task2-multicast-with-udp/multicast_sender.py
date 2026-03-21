import socket
import os
import time
import json
import random

MULTICAST_GROUP = '224.1.1.1'   # same channel receiver is tuned to — must match exactly
PORT = 5007                     # same port receiver is bound to — must match exactly
TTL = 2                         # Time To Live — how many network hops the packet can travel
                                # 2 is enough for container-to-container on the same Docker network
                                # 1 = same subnet only, 32 = same site, 255 = unrestricted

# ============================================================
# create_socket()
# ============================================================
# Purpose: creates and configures a UDP socket for sending
# multicast packets. Sender config is simpler than receiver —
# no bind(), no group membership registration needed.

def create_socket():
    # same as receiver — UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # IPPROTO_IP    - configuring at the IP level
    # IP_MULTICAST_TTL - sets how many network hops the multicast packet can travel
    # TTL = 2, passed directly as an integer (no struct.pack needed in newer Python versions)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)

    return sock

# ============================================================
# send_messages()
# ============================================================
# Purpose: continuously sends two types of messages to the
# multicast group. JSON and binary, until interrupted.
# The sensor type is injected via environment variable so
# the same file can run as temp sender or humidity sender.

def send_messages():
    sock = create_socket()

    # read sensor type from environment variable
    # docker-compose.yml injects SENSOR_TYPE=temp or SENSOR_TYPE=humidity
    # default to 'temp' if not set
    sensor_type = os.environ.get('SENSOR_TYPE', 'temp')

    print(f"Sender started — broadcasting as sensor: {sensor_type}")

    while True:
        # --- JSON message ---
        # build a JSON payload with the sensor type and a random value
        # random.uniform(20.0, 30.0) generates a random float between 20.0 and 30.0
        # round(..., 1) rounds to 1 decimal place e.g. 23.5
        json_message = json.dumps({
            "sensor": sensor_type,
            "value": round(random.uniform(20.0, 30.0), 1)
        })

        # sendto() sends the data to the multicast group
        # .encode('utf-8') converts the string to bytes
        # (MULTICAST_GROUP, PORT) is the destination, the channel and room number
        sock.sendto(json_message.encode('utf-8'), (MULTICAST_GROUP, PORT))
        print("Sent: Multicast message")
        print(f"Sent: {json_message}")

        # --- Binary message ---
        # os.urandom(8) generates 8 cryptographically random bytes
        # this simulates raw binary sensor data (e.g. a packed sensor reading)
        # no encode() needed, it's already bytes
        binary_message = os.urandom(8)
        sock.sendto(binary_message, (MULTICAST_GROUP, PORT))
        print(f"Sent binary data: {binary_message}")

        # wait 1 second between sends so we don't flood the network
        # and so the output is readable in the terminal
        time.sleep(1)

if __name__ == "__main__":
    send_messages()