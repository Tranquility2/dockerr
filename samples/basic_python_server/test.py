import httpx
import os
import sys; sys.path.append(".")  # update python path to include runner module
from runner import DockerRunner

current_dir = os.path.dirname(os.path.realpath(__file__))
test_name = "basic_python_server"
local_url = "http://localhost:9000"

# Test setup
TAG = f"test-{test_name}-image:latest"
NAME = f"test-{test_name}-container"
PORTS = {"9000/tcp": 9000}
PATH = str(current_dir)
DOCKER_FILE = "Dockerfile"

dr = DockerRunner(tag=TAG, name=NAME, ports=PORTS,
                  path=PATH, dockerfile=DOCKER_FILE)


def test_basic_python_server():
    with dr:
        try:
            import time
            time.sleep(0.5)  # Python needs time to load
            response = httpx.get(local_url, timeout=5)
            print("Response:\n", response.text.partition('\n')[0])
        except Exception as e:
            print(f"Response Error: {e}")
            assert False, "Failed to get response"

        assert response.status_code == 200, "Response status code is not 200"

    logs = dr.logs
    assert "GET / HTTP/1.1" in logs, "Request not found in logs"
