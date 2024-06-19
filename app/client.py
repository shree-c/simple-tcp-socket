import socket
from app.logger import logger
from app.config import Config
import sys
from app.utils import read_key, send_message, recv_message





def send_data_to_server(server_public_key, client_private_key, host='127.0.0.1', port=Config.PORT):
    print("Enter data to send to server: ")
    for line in sys.stdin:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        send_message(client_socket, line.strip(), server_public_key)
        
        while True:
            response = recv_message(client_socket, client_private_key)
            if not response:
                break
            print('Received from server:', response)
        client_socket.close()
        print("Enter data to send to server: ")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_public.pem> <client_private.pem>")
        sys.exit(1)

    server_public_key = read_key(sys.argv[1])
    client_private_key = read_key(sys.argv[2])

    if not server_public_key or not client_private_key:
        logger.info("Exiting...")
        sys.exit(1)

    try:
        send_data_to_server(
            client_private_key=client_private_key,
            server_public_key=server_public_key
        )
    except KeyboardInterrupt:
        logger.info("Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
