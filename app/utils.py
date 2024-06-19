from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from time import sleep, strftime, localtime
from app.config import Config
import json
import re


def read_key(file_path):
    try:
        with open(file_path, "rb") as f:
            try:
                return f.read()
            except Exception as e:
                print(f"Error while reading private key: {e}")
    except FileNotFoundError:
        print(f"File {file_path} not found")
    return None


def encrypt_message(message, public_key):
    public_key_obj = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(public_key_obj)
    return cipher.encrypt(message)


def decrypt_message(encrypted_message, private_key):
    private_key_obj = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(private_key_obj)
    return cipher.decrypt(encrypted_message)


def recv_message(client_socket, server_private_key):
    message = client_socket.recv(1024)
    if len(message) == 0:
        return None
    return decrypt_message(message, server_private_key).decode("utf-8")


def send_message(client_socket, message, client_public_key):
    encrypted_message = encrypt_message(message.encode("utf-8"), client_public_key)
    client_socket.sendall(encrypted_message)


def get_current_timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def handle_client_request(
    client_socket,
    request_pattern,
    server_storage,
    server_private,
    client_public,
    sleep_time=1,
):
    try:

        request_parts = recv_message(client_socket, server_private)
        if not re.match(request_pattern, request_parts):
            send_message(client_socket, Config.INVALID_REQUEST_MESSAGE, client_public)
            client_socket.close()

        else:
            request_parts = request_parts.strip().split("-")
            if (
                request_parts[0] in server_storage
                and request_parts[1] in server_storage[request_parts[0]][0]
            ):
                count = server_storage[request_parts[0]][0][request_parts[1]]
                while count > 0:
                    send_message(client_socket, get_current_timestamp(), client_public)
                    sleep(sleep_time)
                    count -= 1
            else:
                send_message(client_socket, Config.DATA_NOT_FOUND_MESSAGE, client_public)
    except Exception as e:
        send_message(client_socket, f"Error: {e}", client_public)
    finally:
        client_socket.close()


def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def read_json_file(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Invalid JSON file")
    except FileNotFoundError:
        print(f"File {file_path} not found")
    return None
