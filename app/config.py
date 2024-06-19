import os
from dotenv import load_dotenv

load_dotenv('settings.env')

class Config:
    PORT = int(os.environ['port'])
    SOCKET_TIMEOUT = float(os.environ['socket_timeout'])
    INCOMING_CONNECTIONS = int(os.environ['incoming_connections'])
    SLEEP_TIME = float(os.environ['sleep_time'])

    SERVER_STORAGE = os.environ['server_storage_path']
    INVALID_REQUEST_MESSAGE = os.environ['invalid_request_message']
    DATA_NOT_FOUND_MESSAGE = os.environ['data_not_found_message']
    INPUT_REGEX = os.environ['input_regex']

    recv_bufsize = int(os.environ['recv_bufsize'])