""" Used to test the DockerRunner with a simple ubuntu echo container"""

import os
import tempfile

from dockerr.runner import DockerRunner

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_NAME = "ubuntu_echo"


# pylint:disable=duplicate-code
def create_dockerfile() -> str:
    """Create a temp Dockerfile"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(
            """
            FROM ubuntu:latest
            CMD echo "Test Dockerfile"
            """
        )
        return f.name


def test_ubunut_echo():
    """Test a simple docker container that echos a string"""
    # Create DockerRunner
    dr = DockerRunner(
        tag=f"test-{TEST_NAME}-image:latest",
        name=f"test-{TEST_NAME}-container",
        path=str(CURRENT_DIR),
        dockerfile=create_dockerfile(),
    )
    # Use DockerRunner as a context manager
    with dr as (name, _):
        print(f"[Container {name} ready]")

    assert dr.logs == "Test Dockerfile\n", "Logs do not match expected output"
