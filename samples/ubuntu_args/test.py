import os
import tempfile
import uuid
import sys; sys.path.append(".")  # update python path to include runner module
from runner import DockerRunner

current_dir = os.path.dirname(os.path.realpath(__file__))
test_name = "ubuntu_args"

ENVIROMENT_ARGS = {
    "TEST_ARG_1": "123",
    "TEST_ARG_2": "test",
    "TEST_ARG_UUID": str(uuid.uuid4()),
}

# create temp linux Dockerfile using tempfile module
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write("""
        FROM ubuntu:latest
        CMD ["printenv"]
    """)
    DOCKER_FILE = f.name

    dr = DockerRunner(tag=f"test-{test_name}-image:latest",
                      name=f"test-{test_name}-container",
                      path=str(current_dir),
                      dockerfile=DOCKER_FILE,
                      env=ENVIROMENT_ARGS)

def test_basic_python_server():
    with dr as (name, id):
        print(f"[Container {name} ready]")

    for key, value in ENVIROMENT_ARGS.items():
        assert f"{key}={value}" in dr.logs, f"Expected env var {key}={value} not found in logs"
