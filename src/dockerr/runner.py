""" Runner module for running docker containers """

from typing import Any

from dockerr.utils.container import Container, ContainerWrapper
from dockerr.utils.docker import DockerWrapper


class RunnerException(Exception):
    """Runner Exception"""


class DockerRunner:
    # pylint:disable=too-many-instance-attributes
    """Docker Runner"""

    def __init__(
        # pylint:disable=too-many-arguments
        self,
        tag: str,
        name: str,
        ports: dict = None,
        env: dict = None,
        path: str = ".",
        dockerfile: str = "Dockerfile",
    ):
        self.tag = tag
        self.name = name

        self.ports = {} if ports is None else ports
        self.env = {} if env is None else env

        self.path = path
        self.dockerfile = dockerfile
        self.prepared = False
        self.logs = None

        self.docker_utils = DockerWrapper()
        self.container: ContainerWrapper = None

    def _prepare(self):
        """Prepare the image"""
        if not self.docker_utils.build_image(tag=self.tag, path=self.path, dockerfile=self.dockerfile):
            raise RunnerException("Image not built!")
        self.prepared = True

    def _remove_dup(self, provide_feedback: bool = True):
        """Remove duplicated container"""

        def get_input():
            """Get user input for removing the duplicated container."""
            return input("Do you want to remove it? (y/n): ").lower()

        try:
            container: Container = self.docker_utils.get_container(self.name)
            if container:
                print(f"Container {self.name} already exists!")
                if get_input() == "y" or not provide_feedback:
                    container_wrap = ContainerWrapper(container)
                    container_wrap.stop()
                    container_wrap.remove()
                    print(f"Container {self.name} stopped and removed!")
                else:
                    raise RunnerException("Cannot proceed with duplicated container! Exiting...")
        except Exception as e:
            raise RunnerException(f"Error while removing duplicated container: {e}") from e

    def _validate(self):
        """Validate preconditions"""
        if not self.prepared:
            raise RunnerException("Image not ready!")
        self._remove_dup()

    def __enter__(self):
        """Run the container"""
        self._prepare()
        self._validate()

        try:
            new_container: Container = self.docker_utils.run_container_detached(
                image=self.tag, name=self.name, ports=self.ports, env=self.env
            )
            self.container = ContainerWrapper(new_container)

            return self.container.name, self.container.id

        except Exception as e:
            raise RunnerException(f"Runner Error: {e}") from e

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
        """Cleanup the container"""
        self.logs = self.container.logs()

        if not self.container:
            raise RunnerException("Container not found!")
        self.container.stop()
        self.container.remove()
