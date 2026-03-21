import socket    # built-in networking library
import struct    # packs data into raw binary for OS-level multicast config
import os        # reads environment variables (DURATION)
import time      # tracks how long the receiver has been running
import json      # parses incoming JSON messages from the sender
import argparse  # parses command line arguments e.g. --duration 45

# 224.x.x.x is a reserved IP range for multicast, like a radio channel
# hardcoded because sender and receiver must agree on the same channel to communicate
MULTICAST_GROUP = '224.1.1.1'

# arbitrary port, just needs to match between sender and receiver
PORT = 5007

def join_multicast_group():
    # creates the socket object, like getting a walkie talkie
    # SOCK_DGRAM = UDP — no handshake, no guaranteed delivery, fire and forget
    # contrast with SOCK_STREAM (TCP) from Task 1 which confirmed every message arrived
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # SOL_SOCKET   - the "level" we're configuring, general socket-level option
    # SO_REUSEADDR - allows the socket to bind to port 5007 even if it was recently
    #                in use (e.g. container crashed and restarted). Without this,
    #                a stale TIME_WAIT state could block the bind for several minutes.
    # 1 - enable, 0 - disable
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind to all network interfaces on this port so we can receive incoming packets
    sock.bind(('', PORT))

    # the OS networking layer is C code that expects multicast membership info packed as raw binary
    # '4sL' format: 4s = 4 byte IP, L = unsigned long for the interface
    # socket.inet_aton converts '224.1.1.1' to 4 bytes
    # INADDR_ANY means use whatever network interface is available
    group = struct.pack('4sL', socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)

    # formally subscribe this container to the multicast group
    # IPPROTO_IP - configuring at IP level, not general socket level
    # IP_ADD_MEMBERSHIP - tells the OS to subscribe this socket to this multicast group ('group')
    # without this, packets sent to 224.1.1.1 are silently ignored
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, group)

    return sock


def receive_messages(duration):
    sock = join_multicast_group()
    print("Joined multicast group")

    # 1 second timeout prevents recvfrom() from blocking forever
    # lets the while loop check the duration condition every second
    sock.settimeout(1.0)
    end_time = time.time() + duration

    while time.time() < end_time:
        try:
            # recvfrom() returns raw bytes + sender's (ip, port)
            # blocks until a packet arrives or the 1 second timeout hits
            data, addr = sock.recvfrom(1024)
            print(f"Received: Multicast message from {addr}")
            # sender broadcasts both JSON and binary; handle both types
            try:
                message = json.loads(data.decode('utf-8'))
                print(f"Received: {message}")
            except (json.JSONDecodeError, UnicodeDecodeError):
                # JSONDecodeError = valid utf-8 but not JSON (shouldn't happen)
                # UnicodeDecodeError = not utf-8 at all, must be binary data
                print(f"Received binary data from {addr}: {data}")

        except socket.timeout:
            # no packet this second, loop back and check duration
            continue

    print("Leaving multicast group")
    sock.close()


if __name__ == "__main__":
    # argparse lets the script accept --duration as a command line argument
    # so we can run: python multicast_receiver.py --duration 45
    # instead of having to set an environment variable
    parser = argparse.ArgumentParser(description='Multicast Receiver')
    parser.add_argument('--duration', type=int, default=60, 
                        help='How long to listen before leaving the multicast group')
    args = parser.parse_args()

    # priority order:
    # 1. DURATION environment variable (set by docker-compose.yml)
    # 2. --duration command line argument (args.duration)
    # 3. default of 60 seconds (defined above in add_argument)
    duration = args.duration
    if os.environ.get('DURATION'):
        # os.environ.get('DURATION', 60) returns DURATION env var if set, otherwise 60
        # int() converts the string value to an integer
        duration = int(os.environ.get('DURATION', 60))
    receive_messages(duration)