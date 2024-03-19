import json
import docker
from docker import DockerClient
from docker.errors import DockerException

from typing import Optional


class DockerUtils:
    def __init__(self):
        self.client: DockerClient = docker.from_env()

    def build_image(self, tag: str, path: str, dockerfile: str = "Dockerfile") -> Optional[str]:
        print("Building image...")
        # image_object, image_logs = self.client.images.build(path=path, dockerfile=dockerfile, tag=tag)
        # Preffer direct API call to get raw output
        try:
            raw_output = self.client.api.build(path=path,
                                               dockerfile=dockerfile,
                                               tag=tag,
                                               decode=True)
        except (DockerException, TypeError) as e:
            print(f"Error: {e}")
            return None

        image_id = None

        for line_dict in raw_output:
            if line_dict.get("stream"):
                print(line_dict["stream"], end="")
            elif line_dict.get("error"):
                print("Error:", line_dict["error"], end="")
            elif line_dict.get("status"):
                print(line_dict["status"], end="")
            elif line_dict.get("aux"):
                image_id = line_dict.get("aux").get("ID")
            else:
                print(json.dumps(line_dict, indent=4))

        if image_id:
            print(f"Image ID: {image_id}")
            return image_id

    def run_container_detached(self, image: str, name: str, ports: dict = {}) -> Optional["ContainerWrapper"]:
        print("Running container...")
        try:
            container = self.client.containers.run(image=image,
                                                   detach=True,
                                                   name=name,
                                                   ports=ports)
            return ContainerWrapper(container)
        except DockerException as e:
            print(f"Error: {e}")
            return None

    def get_container(self, container_id: str) -> Optional["ContainerWrapper"]:
        print("Getting container...")
        try:
            container = self.client.containers.get(container_id)
            return ContainerWrapper(container)
        except DockerException as e:
            print(f"Error: {e}")
            return None


class ContainerWrapper:
    def __init__(self, container: docker.models.containers.Container):
        self.container = container

    def print_logs(self) -> None:
        logs = self.container.logs().decode("utf-8")
        print("Container Logs:")
        for line in logs:
            print(line, end="")

    def stop(self) -> None:
        print("Stopping container...")
        try:
            self.container.stop()
        except DockerException as e:
            print(f"Error: {e}")

    def remove(self) -> None:
        print("Removing container...")
        try:
            self.container.remove()
        except DockerException as e:
            print(f"Error: {e}")
