""" Container related operations"""

from typing import Optional

from docker.errors import DockerException
from docker.models.containers import Container


class ContainerWrapper:
    """Container Wrapper"""

    def __init__(self, container: Container):
        self.container = container
        self.name = container.name
        self.id = container.id

    def logs(self, verbose: bool = True) -> Optional[str]:
        """Get Container Logs"""
        try:
            logs = self.container.logs().decode("utf-8")
            if verbose:
                print("Container Logs:")
                for line in logs:
                    print(line, end="")
            return logs
        except DockerException as e:
            print(f"Error: {e}")
            return None

    def stop(self) -> None:
        """Stop Container"""
        print(f"Stopping {self.name}...")
        try:
            self.container.stop()
        except DockerException as e:
            print(f"Error: {e}")

    def remove(self) -> None:
        """Remove Container"""
        print(f"Removing {self.name}...")
        try:
            self.container.remove()
        except DockerException as e:
            print(f"Error: {e}")
