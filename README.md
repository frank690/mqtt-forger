# NoveltyProducer
[![Build Status](https://travis-ci.org/frank690/NoveltyProducer.svg?branch=master)](https://travis-ci.org/frank690/NoveltyProducer)
[![Coverage Status](https://coveralls.io/repos/github/frank690/NoveltyProducer/badge.svg?branch=master)](https://coveralls.io/github/frank690/NoveltyProducer?branch=master)
[![Documentation Status](https://readthedocs.org/projects/noveltyproducer/badge/?version=latest)](https://noveltyproducer.readthedocs.io/en/latest/?badge=latest)

Use this class to produce artificial data and publish it via mqtt to a specific host.
Each of these datastreams is called a pipeline.
Each pipeline consists of 1-to-n independent channels.
Channels can also be combined into one channel to:
  - increase complexity of the resulting signal.
  - simulate interferences/downtimes/faults with the sending device (e.g. IoT).
  - add noise to the signal.

### How to start a simple data stream.
~~~py
# import class
from NoveltyProducer.Manager import Manager

# init instance
man = Manager()

# create a new pipeline that will send data onto the mqtt topic 'foo' with 15 Hz.
# the data 'bar' is a sinus wave (default setting).
pipe_id = man.create_pipeline(ip_='test.mosquitto.org', port_=1883, topic_='foo', frequency_=15, channel_name_='bar')
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
# new channel 'star' with an sinus wave signal with 2 Hz and minimum value of -3 and maximum value of 5.
# every second (1 Hz) the signal dies and is set to zero for a period of 0.25s.
man.add_channel_to_pipeline(id_=pipe_id, name_='star', frequency_=2, limits_=[-3, 5], dead_frequency_=1, dead_period_=0.25)

# add random noise to the existing channel 'bar'.
man.add_channel_to_pipeline(id_=pipe_id, name_='bar', type_='random', limits_=[-0.5, 0.5])
~~~

### What is streamed.
~~~py
foo b'{"timestamp": "2019-09-05T14:05:39.355935", "bar": 0.0019120901409165336, "star": -1.8889653113514253}'
foo b'{"timestamp": "2019-09-05T14:05:39.422260", "bar": 0.10247297908915542, "star": -2.9902861766885307}'
foo b'{"timestamp": "2019-09-05T14:05:39.482744", "bar": -0.013823800551045262, "star": -1.7001818125099613}'
foo b'{"timestamp": "2019-09-05T14:05:39.550975", "bar": -0.016367015539323848, "star": 0}'
foo b'{"timestamp": "2019-09-05T14:05:39.625205", "bar": 0.15449779561546717, "star": 0}'
foo b'{"timestamp": "2019-09-05T14:05:39.692327", "bar": 0.06736635047192152, "star": 0}'
~~~

### What is left to do.
Check out the [TODO.md](https://github.com/frank690/NoveltyProducer/blob/master/TODO.md).
