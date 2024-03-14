import docker

client = docker.from_env()

def print_containers_status():
    containers_list = client.containers.list()
    print(f"Found {len(containers_list)} containers")
    for container in containers_list:
        print(container.name, container.status)

test_container = client.containers.run("ubuntu", "echo hello world", detach=True)
print(test_container.name, test_container.status)

# List containers
print("Pre:")
print_containers_status()

test_container.remove()

# List containers
print("Post:")
print_containers_status()
