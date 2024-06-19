import socket
import threading
import sys
from app.utils import handle_client_request, read_key, read_json_file
from app.config import Config
from app.logger import logger


def start_server(
    port, private_key, public_key, storage, server_start, listen_start, host="127.0.0.1"
):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        socket.socket.setsockopt(
            server_socket, socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )
        server_socket.bind((host, port))
        logger.info(f"Server started at {host}:{port}")

        server_socket.listen(Config.INCOMING_CONNECTIONS)
        server_socket.settimeout(Config.SOCKET_TIMEOUT)

        listen_start.set()
        try:
            while not server_start.is_set():
                try:
                    logger.info("Waiting for a connection...")
                    # listen_start.set()
                    client_socket, client_address = server_socket.accept()
                except socket.timeout:
                    continue

                # spawn a new thread to handle the client request
                logger.info(f"Connection from {client_address}")
                client_thread = threading.Thread(
                    target=handle_client_request,
                    args=(
                        client_socket,
                        Config.INPUT_REGEX,
                        storage,
                        private_key,
                        public_key,
                        Config.SLEEP_TIME,
                    ),
                )
                client_thread.start()

        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            server_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <server_private.pem> <client_public.pem>")
        sys.exit(1)

    server_private_key = read_key(sys.argv[1])
    client_public_key = read_key(sys.argv[2])

    if not server_private_key or not client_public_key:
        logger.info("Exiting...")
        sys.exit(1)

    server_storage = read_json_file(Config.SERVER_STORAGE)

    if not server_storage:
        logger.info("Exiting...")
        sys.exit(1)

    try:
        start_server(
            port=Config.PORT,
            private_key=server_private_key,
            public_key=client_public_key,
            storage=server_storage,
            server_start=threading.Event(),
            listen_start=threading.Event(),
        )

    except socket.error as e:
        print(f"Socket error: {e}")
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        print(f"Fatal Error: {e}")
    finally:
        logger.info("<Exit>")
