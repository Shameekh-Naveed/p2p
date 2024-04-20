import socket
import threading

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        print(f"Node running on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Connection established with {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            # Receive data from client
            data = client_socket.recv(1024)
            if not data:
                break
            # Process received data
            print(f"Received data: {data.decode('utf-8')}")
            # Echo back to the client
            client_socket.sendall(data)
        client_socket.close()

if __name__ == "__main__":
    # Define host and port
    HOST = 'localhost'
    PORT = 12345

    # Create and start the node
    node = Node(HOST, PORT)
    node.start()
