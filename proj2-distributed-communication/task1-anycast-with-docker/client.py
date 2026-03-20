import socket
import os

# The service names from docker-compose.yml become resolvable hostnames
SERVERS = ["server1", "server2", "server3"]
PORT = 5000

def connect_to_server(hostname):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hostname, PORT))
    response = client.recv(1024).decode('utf-8')
    print(f"Received: {response}")
    client.close()

if __name__ == "__main__":
    for server in SERVERS:
        connect_to_server(server)