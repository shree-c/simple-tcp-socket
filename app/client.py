import socket
from app.config import Config
import sys
from app.utils import read_key, send_message, recv_message

if len(sys.argv) != 3:
    print("Usage: python client.py <server_public.pem> <client_private.pem>")
    sys.exit(1)

print(sys.argv)

server_public_key = read_key(sys.argv[1])
client_private_key = read_key(sys.argv[2])

if not server_public_key or not client_private_key:
    print("Exiting...")
    sys.exit(1)

def send_data_to_server(host='127.0.0.1', port=Config.PORT):
    try:
        for line in sys.stdin:
            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to the server
            client_socket.connect((host, port))
            
            # Send data to the server
            # client_socket.sendall(line.encode('utf-8'))
            send_message(client_socket, line.strip(), server_public_key)
            
            # Receive response from the server (optional)
            # response = client_socket.recv(1024)
            while True:
                response = recv_message(client_socket, client_private_key)
                if not response:
                    break
                print('Received from server:', response)
            
            # Close the connection
            client_socket.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_data_to_server()
