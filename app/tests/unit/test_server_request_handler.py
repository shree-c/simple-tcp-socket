from unittest.mock import MagicMock
from app.utils import handle_client_request, read_json_file
import app.utils as utils
from app.config import Config


def test_handle_client_request(mocker):
    client_socket = MagicMock()
    server_storage = read_json_file(Config.SERVER_STORAGE)
    request_pattern = Config.INPUT_REGEX

    mocker.patch("app.utils.recv_message", return_value="SetA-Two")
    mocker.patch(
        "app.utils.get_current_timestamp",
        side_effect=["2021-07-12 20:00:00", "2021-07-12 20:00:01"],
    )
    mocker.patch("app.utils.send_message", return_value=None)

    handle_client_request(
        client_socket,
        request_pattern,
        server_storage,
        "server_private",
        "client_public",
        0.1,
    )
    assert utils.recv_message.call_count == 1
    assert utils.recv_message.call_args[0][0] == client_socket
    assert utils.recv_message.call_args[0][1] == "server_private"

    assert utils.get_current_timestamp.call_count == 2

    assert utils.send_message.call_count == 2
    assert utils.send_message.call_args_list[0][0][0] == client_socket
    assert utils.send_message.call_args_list[0][0][1] == "2021-07-12 20:00:00"
    assert utils.send_message.call_args_list[1][0][0] == client_socket
    assert utils.send_message.call_args_list[1][0][1] == "2021-07-12 20:00:01"
