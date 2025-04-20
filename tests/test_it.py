import json
import socket
import time

import numpy as np
import pytest

import settings
from server.requests_handler import handler
from server.tcp_server import TCPServer

TEST_HOST = settings.HOST
TEST_PORT = settings.PORT
BUFFER_SIZE = 1024**3
TIMEOUT = 10.0


@pytest.fixture(scope="module", autouse=True)
def use_server():
    server = TCPServer(handler)
    server.start()
    time.sleep(1)
    yield
    server.stop()


def send_request(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)
        s.connect((TEST_HOST, TEST_PORT))
        s.sendall(json.dumps(data).encode("utf-8"))
        response = b""
        while True:
            chunk = s.recv(BUFFER_SIZE)
            if not chunk:
                break
            response += chunk
        return json.loads(response.decode("utf-8"))


@pytest.fixture
def base_input():
    x, y, z = 2, 2, 2
    return {"x": x, "y": y, "z": z, "data": [1.0] * (x * y * z)}


@pytest.fixture
def large_input():
    x, y, z = 30, 30, 10
    return {"x": x, "y": y, "z": z, "data": np.random.rand(x * y * z).tolist()}


def test_basic_processing(base_input):
    response = send_request(base_input)

    assert "processed_data" in response
    assert "stats" in response

    stats = response["stats"]
    assert isinstance(stats["mean"], float)
    assert isinstance(stats["stddev"], float)
    assert isinstance(stats["min"], float)
    assert isinstance(stats["max"], float)


def test_large_data_processing(large_input):
    start_time = time.time()
    response = send_request(large_input)
    processing_time = time.time() - start_time

    assert len(response["processed_data"]) == len(large_input["data"])

    assert processing_time < 5.0


def test_data_integrity():

    test_data = {"x": 1, "y": 1, "z": 4, "data": [1.0, 2.0, 3.0, 4.0]}

    response = send_request(test_data)
    processed = response["processed_data"]

    assert processed != test_data["data"]

    assert all(isinstance(val, float) for val in processed)
