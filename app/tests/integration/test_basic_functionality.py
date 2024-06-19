from app.main import start_server
import re
import pytest
from datetime import datetime
from threading import Thread, Event
import socket
from app.utils import send_message, generate_key_pair, recv_message, read_json_file
from app.config import Config


# make a fixture that generate fours keys
@pytest.fixture
def keys():
    server_private, server_public = generate_key_pair()
    client_private, client_public = generate_key_pair()

    return server_private, server_public, client_private, client_public


@pytest.fixture
def server_thread(keys):
    server_private, _, _, client_public = keys
    # to stop the server thread
    server_start = Event()
    listen_start = Event()

    server_storage = read_json_file(Config.SERVER_STORAGE)
    server_thread = Thread(
        target=start_server,
        args=(
            Config.PORT,
            server_private,
            client_public,
            server_storage,
            server_start,
            listen_start,
        ),
    )

    print("STARTING SERVER.... fixture")
    server_thread.start()
    # wait for the server to start
    yield listen_start.wait()

    server_start.set()
    server_thread.join()


def test_server_responds_correctly_within_given_time(keys, server_thread):
    _, server_public, client_private, __ = keys
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", Config.PORT))

    send_message(client_socket, "SetA-One", server_public)
    received_message = recv_message(client_socket, client_private)
    client_socket.close()

    now = datetime.now()
    received_ts = datetime.strptime(received_message, "%Y-%m-%d %H:%M:%S")

    assert (received_ts.timestamp() - now.timestamp()) < 2


def test_server_responds_correctly_for_given_request(keys, server_thread):
    _, server_public, client_private, __ = keys
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", Config.PORT))

    send_message(client_socket, "SetC-Five", server_public)

    count = 4
    while count > 0:
        received_message = recv_message(client_socket, client_private)
        assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", received_message)

        count -= 1

    client_socket.close()


def test_invalid_request(keys, server_thread):
    _, server_public, client_private, __ = keys
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", Config.PORT))

    send_message(client_socket, "gibbrish123", server_public)
    received_message = recv_message(client_socket, client_private)

    client_socket.close()
    assert received_message == Config.INVALID_REQUEST_MESSAGE

def test_data_not_found(keys, server_thread):
    _, server_public, client_private, __ = keys
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", Config.PORT))

    send_message(client_socket, "Abc-Xyz", server_public)
    received_message = recv_message(client_socket, client_private)

    client_socket.close()
    assert received_message == Config.DATA_NOT_FOUND_MESSAGE
