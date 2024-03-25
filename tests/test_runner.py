"""Test Docker Runner"""

from dockerr.runner import DockerRunner

CONTANIER_NAME = "test_container"
CONTANIER_ID = "test_container_id"


def test_docker_runner():
    """Test Docker Runner"""
    dr = DockerRunner(tag="test_tag", name=CONTANIER_NAME)
    with dr as (c_name, name):
        assert c_name == CONTANIER_NAME, f"Name: {name}"
        assert name == CONTANIER_ID, f"ID: {name}"
        ctr = dr.docker_utils.get_container(CONTANIER_ID)
        assert ctr.status == "running", f"Status: {ctr.status}"
