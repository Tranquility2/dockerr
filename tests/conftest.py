"""Conftest Module"""

from typing import Optional

import pytest
from docker.errors import DockerException


class MockContainer:
    """Mock Container Class"""

    def __init__(self) -> None:
        print("*Init Mock Container*")
        self.name = "test_container"
        self.id = "test_container_id"
        self.status = "initilized"

    def logs(self) -> bytes:
        """Mock Logs Method"""
        return b"[alert] Some test logs\n"

    def stop(self) -> None:
        """Mock Stop Method"""
        self.status = "stopped"

    def remove(self) -> None:
        """Mock Remove Method"""
        self.status = "removed"

    def run(self) -> None:
        """Mock Run Method"""
        self.status = "running"


@pytest.fixture(autouse=True)
def mock_container_obj(monkeypatch) -> None:
    """Mock Container Fixture"""

    def mock_container() -> MockContainer:
        """Mock Container Method"""
        return MockContainer()

    monkeypatch.setattr("docker.models.containers.Container", mock_container, raising=True)


class MockDockerClient:  # pylint: disable=too-few-public-methods
    """Mock Docker Client Class"""

    def __init__(self) -> None:
        print("*Init Mock Docker Client*")

    def from_env(self) -> "MockDockerClient":
        """Mock From Env Method"""

    class api:  # pylint: disable=invalid-name,too-few-public-methods
        """Mock API Class"""

        @staticmethod
        def build(*args, **kwargs) -> None:  # pylint: disable=unused-argument
            """Mock Build Method"""

            return [
                {"stream": "Step 1/2 : FROM python:3.8\n"},
                {"stream": " ---> 2e2f3b6f7a7e\n"},
                {"stream": "Step 2/2 : COPY . /app\n"},
                {"stream": " ---> 2e2f3b6f7a7e\n"},
                {"aux": {"ID": "test_image_id"}},
                {"error": "Some error\n"},
                {"status": "Some status\n"},
                {"unknown": "Some unknown"},
            ]

    class containers:  # pylint: disable=invalid-name,too-few-public-methods
        """Mock Containers Class"""

        @staticmethod
        def run(*args, **kwargs) -> MockContainer:  # pylint: disable=unused-argument
            """Mock Run Method"""
            mock_container = MockContainer()
            mock_container.run()
            return mock_container

        @staticmethod
        def get(container_id) -> Optional[MockContainer]:
            """Mock Get Method"""
            if container_id == "test_container":
                mock_container = MockContainer()
                mock_container.run()
                return mock_container

            raise DockerException("Container not found")


@pytest.fixture(autouse=True)
def mock_docker_from_env(monkeypatch) -> None:
    """Mock Docker Client Fixture"""

    def mock_docker_client() -> MockDockerClient:
        """Mock Docker Client Method"""
        return MockDockerClient()

    monkeypatch.setattr("docker.from_env", mock_docker_client, raising=True)
