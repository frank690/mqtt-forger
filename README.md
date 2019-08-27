# NoveltyProducer
[![Build Status](https://travis-ci.org/frank690/NoveltyProducer.svg?branch=master)](https://travis-ci.org/frank690/NoveltyProducer)
[![Coverage Status](https://coveralls.io/repos/github/frank690/NoveltyProducer/badge.svg?branch=master)](https://coveralls.io/github/frank690/NoveltyProducer?branch=master)

Use this class to produce data and publish it via mqtt to a specific host.
Additionally a random noise can be chosen in frequency, duration and impact to interfere with the produced data.

~~~py
# import class
from NoveltyProducer.Manager import Manager

# init instance
man = Manager()

# create new pipeline that will send data to host onto topic 'foo' with data columns 'bar'. Do this with 15 Hz.
man.create_pipeline('localhost', 1883, 'foo', 15, 'bar')
~~~
