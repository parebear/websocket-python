import asyncio
import threading

import websockets

from src.server.client_manager import ClientManager
from src.server.connection import handle_connection

client_manager = ClientManager()


def run_server_thread(host="localhost", port=8765):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Start the server in this thread's event loop

    async def start_server():
        async def handler(websocket):
            print(f"Connection received")
            await handle_connection(websocket)

        async with websockets.serve(handler, host, port):
            print(f"Websocket server running on {host}:{port}")
            # keep server running
            await asyncio.Future()

    try:
        loop.run_until_complete(start_server())
    except Exception as e:
        print(f"Server error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        loop.close()


def start_server_in_thread():
    server_thread = threading.Thread(target=run_server_thread)
    server_thread.daemon = True
    server_thread.start()
    return server_thread
