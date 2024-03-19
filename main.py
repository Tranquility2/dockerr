import httpx

from docker_utils import DockerUtils
from docker_utils import ContainerWrapper

from docker.models.containers import Container

docker_utils = DockerUtils()


TAG = "test-image:latest"
docker_utils.build_image(tag=TAG, path=".")

try:
    test_container: Container = docker_utils.run_container_detached(image=TAG,
                                                                    name="test-container",
                                                                    ports={"9000/tcp": 9000})

    try:
        import time
        time.sleep(0.5)  # Python needs time to load
        response = httpx.get(f"http://localhost:9000", timeout=5)
        print("Response:\n", response.text.partition('\n')[0])
    except Exception as e:
        print(f"Response Error: {e}")

    conainer_wrap = ContainerWrapper(test_container)

except Exception as e:
    print(f"Container Error: {e}")
finally:
    conainer_wrap.print_logs()
    conainer_wrap.stop()
    conainer_wrap.remove()
