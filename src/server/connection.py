import json

import websockets

from src.server.client_manager import ClientManager

client_manager = ClientManager()


async def handle_connection(websocket):

    client = client_manager.add_client(websocket)

    try:
        # welcome message to just this client

        await client.send({"type": "system", "message": "Welcome to the chat server!"})

        # Announce to everyone else
        await client_manager.broadcast(
            {"type": "system", "message": f"Client {client.client_id} joined"},
            exclude=client.client_id,
        )

        # Process messages
        async for message in websocket:
            print(f"Received from {client.client_id}: {message}")

            try:
                # Try to parse as JSON
                data = json.loads(message)
                # add client  ID to the message
                data["sender"] = client.client_id
                # Broadcast to all clients
                await client_manager.broadcast(data)
            except json.JSONDecodeError:
                # Plain text message
                await client_manager.broadcast(
                    {"type": "message", "sender": client.client_id, "content": message}
                )

    except Exception as e:
        print(f"Error handling client {client.client_id}: {e}")

    finally:
        # Always remove the client when done
        client_manager.remove_client(client.client_id)

        # notify others
        await client_manager.broadcast(
            {"type": "system", "message": f"Client {client.client_id} left"}
        )
