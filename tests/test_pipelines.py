"""This module is used to test the classes in forger.engine.pipelines"""

import pytest

from forger.engine.channels import Channel
from forger.engine.pipelines import Pipeline
from tests.conftest import generator_samples, generator_samples_names, pipeline_samples


@pytest.fixture(
    params=pipeline_samples,
)
def pipeline(request):
    return Pipeline(
        pid=request.param[0],
        ip=request.param[1],
        port=request.param[2],
        topic=request.param[3],
        frequency=request.param[4],
        scheduler=request.param[5],
        name=request.param[6],
    )


@pytest.fixture()
def pipeline_with_channels(pipeline):
    channels = []
    for generator_sample in generator_samples:
        c = pipeline.add_channel(
            name=generator_sample[0],
            frequency=generator_sample[1],
            channel_type=generator_sample[2],
            dead_frequency=generator_sample[3],
            dead_period=generator_sample[4],
            scale=generator_sample[5],
            replay_data=generator_sample[6],
            seed=generator_sample[7],
        )
        channels.append(c)
    return pipeline, channels


class TestPipeline:
    @pytest.mark.parametrize(
        "name,frequency,channel_type,dead_frequency,dead_period,scale,replay_data,seed",
        generator_samples,
    )
    def test_add_channel(
        self,
        pipeline,
        name,
        scale,
        frequency,
        channel_type,
        dead_frequency,
        dead_period,
        replay_data,
        seed,
    ):
        """
        Test the add_channel method of the Pipeline class.
        """
        c1 = pipeline.add_channel(
            name=name,
            scale=scale,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
            replay_data=replay_data,
            seed=seed,
        )

        assert isinstance(c1, Channel)
        assert pipeline.channels.channels[0] == c1

        c2 = pipeline.add_channel(
            name=name,
            scale=scale,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
            replay_data=replay_data,
            seed=seed,
        )

        assert isinstance(c2, Channel)
        assert pipeline.channels.channels[1] == c2

    def test_add_and_remove_channel(self, pipeline_with_channels):
        """
        Test the add_channel and remove_channel methods of the Pipeline class.
        """

        pipeline, channels = pipeline_with_channels

        for c in channels:
            assert isinstance(c, Channel)
        assert len(pipeline.channels.channels) == len(channels)

        for channel in channels:
            pipeline.remove_channel(channel=channel)
        assert len(pipeline.channels.channels) == 0

    def test_add_and_remove_all_channels(self, pipeline_with_channels):
        """
        Test the add_channel and remove_all_channels methods of the Pipeline class.
        """
        pipeline, _ = pipeline_with_channels
        assert len(pipeline.channels.channels) == len(generator_samples)
        pipeline.remove_all_channels()
        assert len(pipeline.channels.channels) == 0

    def test_get_channels(self, pipeline_with_channels):
        """
        Test the get_channels method of the Pipeline class.
        """
        pipeline, _ = pipeline_with_channels
        for generator_samples_name in generator_samples_names:
            channels = pipeline.get_channels(name=generator_samples_name)
            for channel in channels:
                assert isinstance(channel, Channel)
                assert channel.name in generator_samples_names
            assert len(channels) == 4

    def test_switch_state(self, pipeline):
        """
        Test the switch_state method of the Pipeline class.
        """
        assert pipeline.active
        pipeline.switch_state()
        assert not pipeline.active
        pipeline.switch_state(state=True)
        assert pipeline.active
        pipeline.switch_state(state=False)
        assert not pipeline.active

    def test_publish(self, pipeline):
        """
        Test the publish method of the Pipeline class.
        """
        pipeline.publish()
