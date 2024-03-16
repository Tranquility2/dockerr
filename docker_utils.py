import docker
from docker.models.containers import Container


class DockerUtils:
    def __init__(self):
        self.client = docker.from_env()

    def build_image(self, tag, path, dockerfile="Dockerfile") -> str:
        print("Building image...")
        image_object, image_logs = self.client.images.build(path=path,
                                                            dockerfile=dockerfile,
                                                            tag=tag)

        for line in image_logs:
            print(line)

        return image_object.id

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
