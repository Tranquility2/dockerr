from typing import Any

from utils.docker import DockerWrapper
from utils.container import ContainerWrapper, Container


class RunnerException(Exception):
    pass


class DockerRunner:
    def __init__(self, tag: str, name: str, ports: dict = {}, path: str = ".", dockerfile: str = "Dockerfile"):
        self.tag = tag
        self.name = name
        self.ports = ports
        self.path = path
        self.dockerfile = dockerfile
        self.prepared = False
        self.logs = None

        self.docker_utils = DockerWrapper()
        self.container: ContainerWrapper = None

    def _prepare(self):
        if not self.docker_utils.build_image(tag=self.tag, path=self.path, dockerfile=self.dockerfile):
            raise RunnerException("Image not built!")
        self.prepared = True

    def _remove_dup(self, provide_feedback: bool = True):
        def get_input():
            """Get user input for removing the duplicated container."""
            return input("Do you want to remove it? (y/n): ").lower()

        try:
            container: Container = self.docker_utils.get_container(self.name)
            if container:
                print(f"Container {self.name} already exists!")
                if get_input() == "y" or provide_feedback == False:
                    container_wrap = ContainerWrapper(container)
                    container_wrap.stop()
                    container_wrap.remove()
                    print(f"Container {self.name} stopped and removed!")
                else:
                    raise RunnerException(
                        "Cannot proceed with duplicated container! Exiting...")
        except Exception as e:
            raise RunnerException(
                f"Error while removing duplicated container: {e}")

    def _validate(self):
        if not self.prepared:
            raise RunnerException("Image not prepared!")
        self._remove_dup()

    def __enter__(self):
        self._prepare()
        self._validate()

        try:
            new_container: Container = self.docker_utils.run_container_detached(image=self.tag,
                                                                                name=self.name,
                                                                                ports=self.ports)
            self.container = ContainerWrapper(new_container)

            return self.container.name, self.container.id

        except Exception as e:
            raise RunnerException(f"Runner Error: {e}")

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
        self.logs = self.container.logs()

        if not self.container:
            raise RunnerException("Container not found!")
        self.container.stop()
        self.container.remove()
