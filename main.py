import httpx

from docker_utils import DockerUtils

docker_utils = DockerUtils()


TAG = "test-image:latest"
docker_utils.build_image(tag=TAG, path=".")

try:
    test_container_obj = docker_utils.run_container(image=TAG,
                                                    detach=True,
                                                    name="test-container",
                                                    ports={"9000/tcp": 9000})

    try:
        import time
        time.sleep(0.5)  # Python needs time to load
        response = httpx.get(f"http://localhost:9000", timeout=5)
        print("Response:\n", response.text.partition('\n')[0])
    except Exception as e:
        print(f"Response Error: {e}")

    docker_utils.print_logs(test_container_obj)

except Exception as e:
    print(f"Container Error: {e}")
finally:
    docker_utils.stop_container(test_container_obj)
    docker_utils.remove_container(test_container_obj)
