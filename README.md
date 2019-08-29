# NoveltyProducer
[![Build Status](https://travis-ci.org/frank690/NoveltyProducer.svg?branch=master)](https://travis-ci.org/frank690/NoveltyProducer)
[![Coverage Status](https://coveralls.io/repos/github/frank690/NoveltyProducer/badge.svg?branch=master)](https://coveralls.io/github/frank690/NoveltyProducer?branch=master)
[![Documentation Status](https://readthedocs.org/projects/noveltyproducer/badge/?version=latest)](https://noveltyproducer.readthedocs.io/en/latest/?badge=latest)

Use this class to produce data and publish it via mqtt to a specific host.
Additionally a random noise can be chosen in frequency, duration and impact to interfere with the produced data.

### How to start it.
~~~py
# import class
from NoveltyProducer.Manager import Manager

# init instance
man = Manager()

# create new pipeline that will send data onto topic 'foo'.
# do that with 15 Hz.
man.create_pipeline('test.mosquitto.org', 1883, 'foo', 15, 'bar')
~~~

### What it does.
~~~py
foo b'{"timestamp": "2019-08-28T09:38:55.814337", "bar": 0.5487491837412708}'
foo b'{"timestamp": "2019-08-28T09:38:56.821802", "bar": -0.052118018113447295}'
foo b'{"timestamp": "2019-08-28T09:38:57.805056", "bar": -0.620937663401906}'
foo b'{"timestamp": "2019-08-28T09:38:58.811185", "bar": -0.9641198905685163}'
foo b'{"timestamp": "2019-08-28T09:38:59.817089", "bar": -0.9347151370201041}'
foo b'{"timestamp": "2019-08-28T09:39:00.816615", "bar": -0.5475520657645743}'
~~~

### What is left to do.
Check out the [README.md](https://github.com/frank690/NoveltyProducer/blob/master/TODO.md).
