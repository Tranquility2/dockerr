import docker

client = docker.from_env()

def print_containers_status(header: str = "Containers"):
    containers_list = client.containers.list()
    print(f"{header} Found {len(containers_list)} containers")
    for container in containers_list:
        print(f"-> {container.name} [{container.status}]")

test_container = client.containers.run(image="ubuntu", 
                                       remove=True,
                                       detach=True,
                                       tty=True,
                                       name="test-container")
print_containers_status()
test_container_obj = client.containers.get(test_container.id)
run_output = test_container_obj.exec_run("echo 'Hello from the container'")
print(f"Container Output: {run_output.output.decode('utf-8')}")
test_container_obj.stop()
print_containers_status()
