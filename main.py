import docker

client = docker.from_env()

test_container = client.containers.run("ubuntu", "echo hello world", detach=True)
print(test_container.name, test_container.status)

# List containers
print("List(Pre):", client.containers.list())

test_container.remove()

# List containers
print("Lis(Post):", client.containers.list())
