import json
from datetime import datetime


class Client:
    """Represents a connected websocket client."""

    def __init__(self, websocket, client_id=None):
        self.websocket = websocket
        self.client_id = client_id or f"client_id{id(websocket)}"
        self.connected_at = datetime.now()
        self.last_active = self.connected_at
        self.metadata = {}  # for custom data storage

    async def send(self, message):
        """Send a message to this client."""
        if isinstance(message, dict):
            await self.websocket.send(json.dumps(message))
        else:
            await self.websocket.send(str(message))

        self.last_active = datetime.now()

    def is_connected(self):
        """check if client is still connected."""
        return self.websocket.open
