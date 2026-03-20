import socket
import os

def start_server(host='0.0.0.0', port=5000):
    server_id = os.environ.get('SERVER_ID', 'server_unknown')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Accepted connection from ({host}, {port})")

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")
        response = f"Hello from {server_id} !!! "
        client.send(response.encode('utf-8'))
        print(f"Sent: {response}")
        client.close()

if __name__ == "__main__":
    start_server()

