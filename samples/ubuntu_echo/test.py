import os
import tempfile

from dockerr.runner import DockerRunner

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_NAME = "ubuntu_echo"


def test_basic_python_server():
    # Create temp linux Dockerfile
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(
            """
            FROM ubuntu:latest
            CMD echo "Test Dockerfile"
        """
        )
        DOCKER_FILE = f.name
    # Create DockerRunner
    dr = DockerRunner(
        tag=f"test-{TEST_NAME}-image:latest",
        name=f"test-{TEST_NAME}-container",
        path=str(CURRENT_DIR),
        dockerfile=DOCKER_FILE,
    )
    # Use DockerRunner as a context manager
    with dr as (name, id):
        print(f"[Container {name} ready]")

    assert dr.logs == "Test Dockerfile\n", "Logs do not match expected output"
