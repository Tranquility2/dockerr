""" Container related operations"""

from docker.models.containers import Container


class DockerContainerWrapper:
    """Container Wrapper"""

    def __init__(self, container: Container):
        self.container = container
        self.name = container.name
        self.id = container.id

    def logs(self, verbose: bool = True) -> str:
        """Get Container Logs"""
        logs = self.container.logs().decode("utf-8")
        if verbose:
            print("Container Logs:")
            for line in logs:
                print(line, end="")
        return logs

    def stop(self) -> None:
        """Stop Container"""
        print(f"Stopping {self.name}...")
        self.container.stop()

    def remove(self) -> None:
        """Remove Container"""
        print(f"Removing {self.name}...")
        self.container.remove()
