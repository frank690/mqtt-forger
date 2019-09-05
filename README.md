# NoveltyProducer
[![Build Status](https://travis-ci.org/frank690/NoveltyProducer.svg?branch=master)](https://travis-ci.org/frank690/NoveltyProducer)
[![Coverage Status](https://coveralls.io/repos/github/frank690/NoveltyProducer/badge.svg?branch=master)](https://coveralls.io/github/frank690/NoveltyProducer?branch=master)
[![Documentation Status](https://readthedocs.org/projects/noveltyproducer/badge/?version=latest)](https://noveltyproducer.readthedocs.io/en/latest/?badge=latest)


Use this class to produce artificial data and publish it via mqtt to a specific host.


### How to start a simple data stream.
~~~py
# import class
from NoveltyProducer.Manager import Manager

# init instance
man = Manager()

# create a new pipeline that will send data onto the mqtt topic 'foo' with 15 Hz.
# the data 'bar' is a sinus wave (default setting).
pipe_id = man.create_pipeline('test.mosquitto.org', 1883, 'foo', 15, 'bar')
~~~


### What is streamed.
~~~py
foo b'{"timestamp": "2019-08-28T09:38:55.814337", "bar": 0.5487491837412708}'
foo b'{"timestamp": "2019-08-28T09:38:56.821802", "bar": -0.052118018113447295}'
foo b'{"timestamp": "2019-08-28T09:38:57.805056", "bar": -0.620937663401906}'
foo b'{"timestamp": "2019-08-28T09:38:58.811185", "bar": -0.9641198905685163}'
foo b'{"timestamp": "2019-08-28T09:38:59.817089", "bar": -0.9347151370201041}'
foo b'{"timestamp": "2019-08-28T09:39:00.816615", "bar": -0.5475520657645743}'
~~~


### Add another channel to the existing pipeline. Also add random noise to 'bar'.
~~~py
# add channel 'star'. 2 Hz sin-wave with altitudes of -3 to +5.
# signal dies with 1 Hz for a period of 0.25s.
man.add_channel_to_pipeline(pipe_id, 'star', [-3, 5], 2, 'sin', 1, 0.25)

# add random noise to the existing channel 'bar'.
man.add_channel_to_pipeline(pipe_id, 'bar', [-0.5, 0.5], 'random')
~~~


### What is streamed.
~~~py
foo b'{"timestamp": "2019-09-05T14:05:39.355935", "bar": 0.0019120901409, "star": -1.888965311351}'
foo b'{"timestamp": "2019-09-05T14:05:39.422260", "bar": 0.1024729790856, "star": -2.990286176688}'
foo b'{"timestamp": "2019-09-05T14:05:39.482744", "bar": -0.0138238005510, "star": -1.700181812509}'
foo b'{"timestamp": "2019-09-05T14:05:39.550975", "bar": -0.0163670155393, "star": 0}'
foo b'{"timestamp": "2019-09-05T14:05:39.625205", "bar": 0.1544977956158, "star": 0}'
foo b'{"timestamp": "2019-09-05T14:05:39.692327", "bar": 0.0673663504719, "star": 0}'
~~~


### What is left to do.
Check out the [TODO.md](https://github.com/frank690/NoveltyProducer/blob/master/TODO.md).
