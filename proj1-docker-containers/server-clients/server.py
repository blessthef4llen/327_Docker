# import socket library - Python's networking module for TCP/UDP communication
import socket 


def start_server(host='0.0.0.0', port=5000):
    """
    Start a server that listens for incoming connections.

    Parameters:
    host (str): The hostname or IP address the server binds to.
                Default is '0.0.0.0', which means it listens on all available interfaces.
    port (int): The port number on which the server listens.
                Default is 5000.

    Returns:
    None: This function does not return a value.
    """

    # Create TCP socket
    # AF_INET = IPv4 address
    # SOCK_STREAM = TCP (SOCK_DGRAM for UDP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind socket to address and port - "listen on 0.0.0.0:5000"
    server.bind((host, port))

    # Start listening for connections
    # 5 = max queued connections (if 5 clients connecting simultaneously, 6th waits)
    server.listen(5)

    # Log message - confirms server started
    print(f"Server listening on {host}:{port}")

    while True: # server runs forever, accepting connections

        # wait for client connection (blocks here until someone connects)
        # client = socket for this specific client
        # addr = client's IP address and port
        client, addr = server.accept()

        # log which client connected
        print(f"Connection from {addr}")

        # receive data from client
        # recv(1024) = read up to 1024 bytes
        # .decode('utf-8') = convert bytes to string
        data = client.recv(1024).decode('utf-8')

        # log what client sent
        print(f"Received: {data}")

        # send response back to client
        # f"Echo: {data}" = prepend "Echo: " to message
        # .encode('utf-8') = convert string to bytes for transmission
        response = f"Echo: {data}"
        client.send(response.encode('utf-8'))

        # close client connection - loop then continues to accept next client
        client.close()

# run server when script executed directly
if __name__ == "__main__":
    start_server()