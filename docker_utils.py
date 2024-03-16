import json
import docker
from docker.models.containers import Container
from docker.models.images import Image

from typing import Optional


class DockerUtils:
    def __init__(self):
        self.client = docker.from_env()

    def build_image(self, tag, path, dockerfile="Dockerfile") -> Optional[str]:
        print("Building image...")
        # image_object, image_logs = self.client.images.build(path=path, dockerfile=dockerfile, tag=tag)
        # Preffer direct API call to get live logs
        live_logs = self.client.api.build(path=path,
                                          dockerfile=dockerfile,
                                          tag=tag,
                                          decode=True)

        image_id = None

        for line_dict in live_logs:
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

    def run_container(self, image, detach, name, ports) -> Container:
        print("Running container...")
        container = self.client.containers.run(image=image,
                                               detach=detach,
                                               name=name,
                                               ports=ports)
        return container

    def get_container(self, container_id) -> Container:
        print("Getting container...")
        container = self.client.containers.get(container_id)
        return container

    def print_logs(self, container: Container) -> None:
        logs = container.logs().decode("utf-8")
        print("Container Logs:\n", logs)

    def stop_container(self, container: Container):
        print("Stopping container...")
        container.stop()

    def remove_container(self, container: Container):
        print("Removing container...")
        container.remove()
