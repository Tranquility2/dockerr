""" Runner module for running docker containers """

from typing import Any, Optional

from dockerr.utils.container import DockerContainerWrapper
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
        ports: Optional[dict] = None,
        env: Optional[dict] = None,
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
        self.logs: Optional[str] = None
        self.docker_utils = DockerWrapper()
        self.container: Optional[DockerContainerWrapper] = None

    def _prepare(self) -> None:
        """Prepare the image"""
        if not self.docker_utils.build_image(tag=self.tag, path=self.path, dockerfile=self.dockerfile):
            raise RunnerException("Image not built!")
        self.prepared = True

    def _remove_dup(self, provide_feedback: bool = True) -> None:
        """Remove duplicated container"""

        def get_input() -> str:
            """Get user input for removing the duplicated container."""
            return input("Do you want to remove it? (y/n): ").lower()

        try:
            container = self.docker_utils.get_container(self.name)
            if container:
                print(f"Container {self.name} already exists!")
                if get_input() == "y" or not provide_feedback:
                    container_wrap = DockerContainerWrapper(container)
                    container_wrap.stop()
                    container_wrap.remove()
                    print(f"Container {self.name} stopped and removed!")
                else:
                    raise RunnerException("Cannot proceed with duplicated container! Exiting...")
        except Exception as e:
            raise RunnerException(f"Error while removing duplicated container: {e}") from e

    def _validate(self) -> None:
        """Validate preconditions"""
        if not self.prepared:
            raise RunnerException("Image not ready!")
        self._remove_dup()

    def __enter__(self) -> tuple[str, str]:
        """Run the container"""
        self._prepare()
        self._validate()

        try:
            new_container = self.docker_utils.run_container_detached(
                image=self.tag, name=self.name, ports=self.ports, env=self.env
            )
            self.container = DockerContainerWrapper(new_container)

            return self.container.name, self.container.id

        except Exception as e:
            raise RunnerException(f"Runner Error: {e}") from e

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Cleanup the container"""
        if not self.container:
            raise RunnerException("Container not found!")
        # Save logs
        self.logs = self.container.logs()
        # Stop and remove container
        self.container.stop()
        self.container.remove()
