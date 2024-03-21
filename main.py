import httpx

from runner import DockerRunner


TAG = "test-image:latest"
NAME = "test-container"
PORTS = {"9000/tcp": 9000}
PATH = "."
DOCKER_FILE = "Dockerfile"

docker_runner = DockerRunner(
    tag=TAG, name=NAME, ports=PORTS, path=PATH, dockerfile=DOCKER_FILE)

def test_sample():
    print("[Testing sample]")
    try:
        import time
        time.sleep(0.5)  # Python needs time to load
        response = httpx.get(f"http://localhost:9000", timeout=5)
        print("Response:\n", response.text.partition('\n')[0])
    except Exception as e:
        print(f"Response Error: {e}")
    print("[Test End]")

with docker_runner as (name, id):
    print(f"[Container ready]")
    test_sample()

exit(0)
