import os
import tempfile
import sys; sys.path.append(".")  # update python path to include runner module
from runner import DockerRunner

current_dir = os.path.dirname(os.path.realpath(__file__))
test_name = "ubuntu_echo"

# create temp linux Dockerfile using tempfile module
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write("""
        FROM ubuntu:latest
        CMD echo "Test Dockerfile"
    """)
    DOCKER_FILE = f.name

    dr = DockerRunner(tag=f"test-{test_name}-image:latest",
                      name=f"test-{test_name}-container",
                      path=str(current_dir),
                      dockerfile=DOCKER_FILE)


def test_basic_python_server():
    with dr as (name, id):
        print(f"[Container {name} ready]")

    assert dr.logs == "Test Dockerfile\n", "Logs do not match expected output"
