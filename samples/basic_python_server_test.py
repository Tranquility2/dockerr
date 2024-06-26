"""Used to test the DockerRunner with a simple python server running in a docker container"""

import os
import time

import httpx

from dockerr.runner import DockerRunner

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DOCKER_FILE_DIR = os.path.join(CURRENT_DIR, "basic_python_server")
TEST_NAME = "basic_python_server"
LOCAL_URL = "http://localhost:9000"

# Test setup
TAG = f"test-{TEST_NAME}-image:latest"
NAME = f"test-{TEST_NAME}-container"
PORTS = {"9000/tcp": 9000}
PATH = DOCKER_FILE_DIR
DOCKER_FILE = "Dockerfile"


def test_basic_python_server():
    """Test a simple python server running in a docker container"""
    # Create DockerRunner
    dr = DockerRunner(tag=TAG, name=NAME, ports=PORTS, path=PATH, dockerfile=DOCKER_FILE)
    # Use DockerRunner as a context manager
    with dr:
        try:
            time.sleep(0.5)  # Python needs time to load
            response = httpx.get(LOCAL_URL, timeout=5)
            print("Response:\n", response.text.partition("\n")[0])
        except httpx.HTTPError as e:
            print(f"Response Error: {e}")
            assert False, "Failed to get response"

        assert response.status_code == 200, "Response status code is not 200"

    logs = dr.logs
    assert "GET / HTTP/1.1" in logs, "Request not found in logs"
