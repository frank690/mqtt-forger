# NoveltyProducer
Use this class to produce data and publish it via mqtt to a specific host.
Additionally a random noise can be chosen in frequency, duration and impact to interfere with the produced data.

~~~py
# import class
from NoveltyProducer import NoveltyProducer

# init instance
nov = NoveltyProducer()

# create new pipeline that will send data to host onto topic 'foo' with data columns 'bar'. Do this with 15 Hz.
nov.create_pipeline('1.234.567.89', 1883, 'foo', 15, 'bar')
~~~
