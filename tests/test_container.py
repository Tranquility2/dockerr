"""Test Container Wrapper"""

from dockerr.utils.container import DockerContainerWrapper
from tests.conftest import MockContainer


def test_container_wrapper_init() -> None:
    """Test Container Wrapper Init"""
    cw = DockerContainerWrapper(MockContainer())
    assert cw.name == "test_container", f"Name: {cw.name}"
    assert cw.id == "test_container_id", f"ID: {cw.id}"


def test_container_wrapper_logs() -> None:
    """Test Container Wrapper Logs"""
    container = DockerContainerWrapper(MockContainer())
    logs = container.logs()
    assert logs == "[alert] Some test logs\n", f"Logs: {logs}"


def test_container_wrapper_stop() -> None:
    """Test Container Wrapper Stop"""
    container = DockerContainerWrapper(MockContainer())
    container.stop()
    assert container.container.status == "stopped", f"Status: {container.container.status}"


def test_container_wrapper_remove() -> None:
    """Test Container Wrapper Remove"""
    container = DockerContainerWrapper(MockContainer())
    container.remove()
    assert container.container.status == "removed", f"Status: {container.container.status}"
