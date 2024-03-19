from docker.models.containers import Container
from docker.errors import DockerException


class ContainerWrapper:
    def __init__(self, container: Container):
        self.container = container
        self.name = container.name

    def print_logs(self) -> None:
        try:
            logs = self.container.logs().decode("utf-8")
            print("Container Logs:")
            for line in logs:
                print(line, end="")
        except DockerException as e:
            print(f"Error: {e}")

    def stop(self) -> None:
        print(f"Stopping {self.name}...")
        try:
            self.container.stop()
        except DockerException as e:
            print(f"Error: {e}")

    def remove(self) -> None:
        print(f"Removing {self.name}...")
        try:
            self.container.remove()
        except DockerException as e:
            print(f"Error: {e}")
