"""This module is used to test the classes in forger.engine.manager"""

import pytest

from forger.engine.manager import Manager
from forger.engine.pipelines import Pipeline
from tests.conftest import pipeline_samples, pipeline_samples_names


@pytest.fixture()
def manager():
    man = Manager()
    man.Scheduler.pause()
    return man


@pytest.fixture()
def manager_with_pipelines(manager):
    pipelines = []
    for pipeline_sample in pipeline_samples:
        pipelines.append(
            manager.add_pipeline(
                ip=pipeline_sample[1],
                port=pipeline_sample[2],
                topic=pipeline_sample[3],
                frequency=pipeline_sample[4],
                pipeline_name=pipeline_sample[6],
            )
        )
    return manager, pipelines


class TestManager:
    def test_add_pipeline(self, manager_with_pipelines):
        """
        Test the add_pipeline method of the Manager class.
        """
        manager, pipelines = manager_with_pipelines
        for pipeline in pipelines:
            assert isinstance(pipeline, Pipeline)
            assert manager.pipelines[pipeline.pid] == pipeline

    def test_get_names(self, manager_with_pipelines):
        """
        Test the get_names method of the Manager class.
        """
        manager, _ = manager_with_pipelines
        names = manager.get_names()
        assert set(names) == set(pipeline_samples_names)
