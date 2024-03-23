""" Used to test the DockerRunner with a simple ubuntu echo container"""

import os
import tempfile
import uuid

from dockerr.runner import DockerRunner

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_NAME = "ubuntu_args"
ENVIROMENT_ARGS = {
    "TEST_ARG_1": "123",
    "TEST_ARG_2": "test",
    "TEST_ARG_UUID": str(uuid.uuid4()),
}


# pylint:disable=duplicate-code
def create_dockerfile() -> str:
    """Create a temp Dockerfile"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(
            """
            FROM ubuntu:latest
            CMD ["printenv"]
            """
        )
        return f.name


def test_ubuntu_args():
    """Test a simple docker container that prints env vars"""
    # Create DockerRunner
    dr = DockerRunner(
        tag=f"test-{TEST_NAME}-image:latest",
        name=f"test-{TEST_NAME}-container",
        path=str(CURRENT_DIR),
        dockerfile=create_dockerfile(),
        env=ENVIROMENT_ARGS,
    )
    # Use DockerRunner as a context manager
    with dr as (name, _):
        print(f"[Container {name} ready]")

    for key, value in ENVIROMENT_ARGS.items():
        assert f"{key}={value}" in dr.logs, f"Expected env var {key}={value} not found in logs"
