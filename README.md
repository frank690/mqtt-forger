# mqtt-forger
[![Build Status](https://travis-ci.org/frank690/mqtt-forger.svg?branch=master)](https://travis-ci.org/frank690/mqtt-forger)
[![Coverage Status](https://coveralls.io/repos/github/frank690/mqtt-forger/badge.svg?branch=master)](https://coveralls.io/github/frank690/mqtt-forger?branch=master)
[![Documentation Status](https://readthedocs.org/projects/mqtt-forger/badge/?version=latest)](https://mqtt-forger.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Use this class to produce artificial data and publish it via mqtt to a specific host.


#### How to start a simple data stream.
~~~py
# import class
from transmitter.engine import Manager

# init manager instance
man = Manager()

# create a new pipeline that will send data onto the mqtt topic 'foo' with 15 Hz.
pipeline = man.add_pipeline(ip='test.mosquitto.org', port=1883, topic='foo', frequency=15)

# attach a function/channel to the just created pipeline that will produce a 
# sin-wave with an lower bound of -1 and upper bound of 3.
# The sine wave will have an 0.5 Hz frequency.
channel_1 = pipeline.add_channel(name='bar', limits=[-1, 3], frequency=0.5)
~~~

#### What is streamed.
~~~py
foo b'{"timestamp": "2019-08-28T09:38:55.814337", "bar": 0.5487491837412708}'
foo b'{"timestamp": "2019-08-28T09:38:56.821802", "bar": -0.052118018113447295}'
foo b'{"timestamp": "2019-08-28T09:38:57.805056", "bar": -0.620937663401906}'
foo b'{"timestamp": "2019-08-28T09:38:58.811185", "bar": -0.9641198905685163}'
foo b'{"timestamp": "2019-08-28T09:38:59.817089", "bar": -0.9347151370201041}'
foo b'{"timestamp": "2019-08-28T09:39:00.816615", "bar": -0.5475520657645743}'
~~~

#### How to visualize the data flow.
~~~py
# import class
from transmitter.engine import Painter

# init painter instance and listen to specific host ip, port and mqtt topic.
Painter('test.mosquitto.org', 1883, 'foo')
~~~

![Single Channel](img/example_1.png)

#### Stack and/or add channels
~~~py
# add noise to the already existing channel 'bar'
noisy_channel = pipeline.add_channel(name='bar', channel_type='random')

# add another sine-wave as a new channel 'baz'. 
# this channel has a dead time of 1 second. occuring every 2 seconds.
another_channel_id = pipeline.add_channel(name='baz', dead_frequency=0.5, dead_period=1)
~~~

![Multiple Channels](img/example_2.png)

#### Stream your own dataset.
~~~py
# import numpy to generate some data
import numpy as np

# it is also possible to replay your own list of datapoints.
data = [np.tanh(x) for x in np.linspace(-2, 2, 100)]

# add another new channel 'qux' that replays the previously generated dataset.
# it is a good habit to define a frequency so you know the speed at which your data will be streamed.
replay_channel = pipeline.add_channel(name='qux', replay_data=data, frequency=0.1)
~~~


#### Remove one or all channels
~~~py
# either by still having the object itself (e.g. replay_channel from example above)
pipeline.remove_channel(channel=replay_channel)

# or by getting all channels that stream onto a certain name
forgotten_channels = pipeline.get_channels(name="bar")  # this returns [channel_1, noisy_channel]

# or just by removing all channels of a pipeline (topic)
pipeline.remove_all_channels()
~~~

#### What is left to do.
Check out the [TODO.md](https://github.com/frank690/mqtt-forger/blob/master/TODO.md).
