import httpx

from utils.docker import DockerWrapper
from utils.container import ContainerWrapper

from docker.models.containers import Container

docker_utils = DockerWrapper()


TAG = "test-image:latest"
NAME = "test-container"
docker_utils.build_image(tag=TAG, path=".")

# check for running container with the same name
try:
    container: Container = docker_utils.get_container(NAME)
    if container:
        print(f"Container {NAME} already exists!")
        container_wrap = ContainerWrapper(container)
        container_wrap.stop()
        container_wrap.remove()
        print(f"Container {NAME} stopped and removed!")
except Exception as e:
    print(f"Container Error: {e}")


try:
    test_container: Container = docker_utils.run_container_detached(image=TAG,
                                                                    name=NAME,
                                                                    ports={"9000/tcp": 9000})
    conainer_wrap = ContainerWrapper(test_container)

    try:
        import time
        time.sleep(0.5)  # Python needs time to load
        response = httpx.get(f"http://localhost:9000", timeout=5)
        print("Response:\n", response.text.partition('\n')[0])
    except Exception as e:
        print(f"Response Error: {e}")


except Exception as e:
    print(f"Container Error: {e}")
finally:
    conainer_wrap.logs()
    conainer_wrap.stop()
    conainer_wrap.remove()
