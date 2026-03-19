# import socket library - Python's networking module for TCP/UDP communication
import socket 

def send_message(message, host='server', port=5000):
    """
    Send a message to the specified server.

    Parameters:
    message (str): The message to be sent to the server.
    host (str): The hostname or IP address of the server.
                Default is 'server'.
    port (int): The port number on which the server is listening for incoming mesages.
                Default is 5000.

    Returns:
    None: This function does not return a value.
    """

    # Create TCP socket
    # Same as server (server.py)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server - establishes TCP connection to server:5000
    client.connect((host, port))

    # Send message to server - encodes strings to bytes, transmits
    client.send(message.encode('utf-8'))

    # Receive server's response - reads up to 1024 bytes, decodes to string
    response = client.recv(1024).decode('utf-8')

    # Log conversation - shows what was sent and what came back
    print(f"Sent: {message}")
    print(f"Received: {response}")

    # Close connection
    client.close()

if __name__ == "__main__":
    send_message("Hello from our group!")

