import socket
import threading
import hashlib


class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = {}  # Dictionary to store key-value pairs

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        print(f"Node running on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Connection established with {client_address}")
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            # Receive data from client
            data = client_socket.recv(1024)
            if not data:
                break
            # Process received data
            decoded_data = data.decode('utf-8')
            if decoded_data.startswith("PUT"):
                _, key, value = decoded_data.split()
                self.put(key, value)
                response = "Stored successfully."
            elif decoded_data.startswith("GET"):
                _, key = decoded_data.split()
                response = self.get(key)
            else:
                response = "Invalid command."
            # Send response back to the client
            client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    def put(self, key, value):
        # Hash the key to determine which node should store it
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        # Assuming 1000 nodes in the network
        node_id = int(hashed_key, 16) % 1000
        self.data[node_id] = value

    def get(self, key):
        # Hash the key to determine which node should retrieve it
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        # Assuming 1000 nodes in the network
        node_id = int(hashed_key, 16) % 1000
        return self.data.get(node_id, "Key not found.")


if __name__ == "__main__":
    # Define host and port
    HOST = 'localhost'
    PORT = 12345

    # Create and start the node
    node = Node(HOST, PORT)
    node.start()
