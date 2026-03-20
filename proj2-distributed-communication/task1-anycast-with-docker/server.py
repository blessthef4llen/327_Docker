import socket

def start_server(host='0.0.0.0', port=5000):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((host, port))

    server.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:

        client, addr = server.accept()

        response = "Hello from server1 !!! "

        client.send(response.encode('utf-8'))

        client.close()


if __name__ == "__main__":
    start_server()

