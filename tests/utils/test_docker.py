"""Test Docker Wrapper"""

from dockerr.utils.docker import DockerWrapper


def test_docker_wrapper():
    """Test Docker Wrapper"""
    dw = DockerWrapper()
    assert dw.client is not None


def test_docker_wrapper_build_image(capfd):
    """Test Docker Wrapper Build Image"""
    dw = DockerWrapper()
    image_id = dw.build_image("test_image", "tests/test_data")
    out, _ = capfd.readouterr()
    assert image_id == "test_image_id", f"Image ID: {image_id}"
    assert "Building image..." in out
    assert "Step 1/2 : FROM python:3.8" in out
    assert "Step 2/2 : COPY . /app" in out
    assert "Image ID: test_image_id" in out
    assert "Some error" in out
    assert "Some status" in out
    assert "Some unknown" in out


def test_docker_wrapper_run_container_detached(capfd):
    """Test Docker Wrapper Run Container Detached"""
    dw = DockerWrapper()
    container = dw.run_container_detached("test_image", "test_container")
    out, _ = capfd.readouterr()
    assert container.name == "test_container", f"Name: {container.name}"
    assert container.status == "running", f"Status: {container.status}"
    assert "Running container..." in out


def test_docker_wrapper_docker_get_containers():
    """Test Docker Wrapper Get Containers"""
    dw = DockerWrapper()
    containers = dw.get_container("test_container")
    assert containers.name == "test_container", f"Name: {containers.name}"
    assert containers.status == "running", f"Status: {containers.status}"


def test_docker_wrapper_docker_get_containers_exception():
    """Test Docker Wrapper Get Containers Exception"""
    dw = DockerWrapper()
    containers = dw.get_container("no_container")
    assert containers is None, f"Containers: {containers}"
