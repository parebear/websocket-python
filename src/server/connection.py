import websockets


async def handle_connection(websocket):
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except Exception as e:
        print(f"Error in connection handler: {e}")
