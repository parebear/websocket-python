# Add project to the Python path
import time

from src.server.websocket_server import start_server_in_thread

if __name__ == "__main__":
    print("starting server thread...")
    server_thread = start_server_in_thread()
    print("Server started in background thread")

    print("server thread started, main thread continuing")

    # keep the main thread alive
    try:
        while True:
            time.sleep(1)
            if not server_thread.is_alive():
                print("server died for some reason")
                break
    except KeyboardInterrupt:
        print("\nShutting down server...")
