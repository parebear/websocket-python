import threading

from src.models.client import Client


class ClientManager:
    """Manages WebSocket client connections."""

    def __init__(self):
        self.clients = {}  # maps client_id to client objects
        self.lock = threading.Lock()

    def add_client(self, websocket, client_id=None):
        """Register new client"""
        client = Client(websocket, client_id)

        with self.lock:
            self.clients[client.client_id] = client

        print(f"Client {client.client_id} connected")
        return client

    def remove_client(self, client_id):
        """Remove a client connection"""

        with self.lock:
            if client_id in self.clients:
                del self.clients[client_id]
                print(f"Client {client_id} disconnected")

    def get_client(self, client_id):

        with self.lock:
            return self.clients.get(client_id)

    def get_all_clients(self):
        """Get all active clients"""
        with self.lock:
            return list(self.clients.values())

    async def broadcast(self, message, exclude=None):
        """Send a message to all connected clients."""
        clients_to_remove = []

        with self.lock:
            clients = list(self.clients.values())

        for client in clients:
            if exclude and client.client_id == exclude:
                continue

            try:
                await client.send(message)
            except Exception as e:
                print(f"Error sending to {client.client_id}: {e}")
                clients_to_remove.append(client.client_id)

        for client_id in clients_to_remove:
            self.remove_client(client_id)
