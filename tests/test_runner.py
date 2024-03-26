"""Test Docker Runner"""

import pytest

from dockerr.runner import DockerRunner, RunnerException

CONTANIER_NAME = "test_container"
CONTANIER_ID = "test_container_id"


def test_docker_runner():
    """Test Docker Runner"""
    dr = DockerRunner(tag="test_tag", name=CONTANIER_NAME)
    dr.provide_feedback = False
    with dr as (c_name, c_id):
        assert c_name == CONTANIER_NAME, f"Name: {c_name}"
        assert c_id == CONTANIER_ID, f"ID: {c_id}"
        ctr = dr.docker_utils.get_container(CONTANIER_NAME)
        assert ctr.status == "running", f"Status: {ctr.status}"


def test_docker_runner_feedback(monkeypatch):
    """Test Docker Runner"""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    dr = DockerRunner(tag="test_tag", name=CONTANIER_NAME)
    dr.provide_feedback = True  # Default value
    with pytest.raises(RunnerException):
        with dr as (c_name, c_id):
            assert c_name == CONTANIER_NAME, f"Name: {c_name}"
            assert c_id == CONTANIER_ID, f"ID: {c_id}"


def test_docker_runner_missing_container():
    """Test Docker Runner"""
    dr = DockerRunner(tag="test_tag", name="missing_container")
    with pytest.raises(RunnerException):
        with dr as (c_name, c_id):
            assert c_name == CONTANIER_NAME, f"Name: {c_name}"
            assert c_id == CONTANIER_ID, f"ID: {c_id}"
            dr.container = None
