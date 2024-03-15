import docker
import httpx

from docker.models.containers import Container

client = docker.from_env()

def print_containers_status(header: str = "(Containers)"):
    containers_list = client.containers.list()
    print(f"{header} Found {len(containers_list)}")
    for container in containers_list:
        print(f"-> {container.name} [{container.status}]")


TAG = "test-image:latest"
image_object, image_logs = client.images.build(path=".",
                                               dockerfile="Dockerfile",
                                               tag=TAG)

for line in image_logs:
    print(line)

print(f"image: {image_object.id}")

try:
    test_container = client.containers.run(image=TAG,
                                           detach=True,
                                           name="test-container",
                                           ports={"9000/tcp": 9000})
    print_containers_status()
    test_container_obj : Container = client.containers.get(test_container.id)

    try:
        import time; time.sleep(0.2) # Python needs time to load
        response = httpx.get(f"http://localhost:9000", timeout=5)
        print("Response:\n", response.text.partition('\n')[0])
    except Exception as e:
        print(f"Response Error: {e}")

    print("Container Logs:\n", test_container_obj.logs().decode("utf-8"))

except Exception as e:
    print(f"Container Error: {e}")
finally:
    test_container_obj.stop()
    test_container_obj.remove()
