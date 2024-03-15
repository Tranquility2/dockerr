import docker

client = docker.from_env()

def print_containers_status(header: str = "Containers"):
    containers_list = client.containers.list()
    print(f"{header} Found {len(containers_list)} containers")
    for container in containers_list:
        print(f"-> {container.name} [{container.status}]")

test_container = client.containers.run("ubuntu", "echo hello world", detach=True)
print(test_container.name, test_container.status)


print_containers_status(header="(Pre)")

test_container.remove()

print_containers_status(header="(Post)")
