#!/usr/bin/env python3

from Generator import Generator
from apscheduler.schedulers.background import BackgroundScheduler
import paho.mqtt.client as mqtt

class NoveltyProducer:
    """
    Class to connect to a given host and send data with a given frequency.
    This data may include regulary appearing novelties.
    """
    def __init__(self, verbose_=False):
        # init handlers
        self.Scheduler = BackgroundScheduler()
        # start scheduler
        self.Scheduler.start()        
        # init dict for handlers, pipelines, connections, topics, channels and novelties
        self.handlers = {} # contains instances of Generator
        self.pipelines = {} # contains ids of host, topic, ...
        self.connections = {} # contains host informations
        self.topics = {} # contains topic informations
        self.channels = {} # contains channel informations
        self.novelties = {} # contains novelty informations
        # init parameters
        self.verbose = verbose_

    def create_pipeline(self, ip_, port_, topic_, frequency_, channel_name_, \
        channel_limits_=[-1, 1], channel_frequency_=0.1, novelty_frequency_=0.0167, \
        novelty_duration_=5, novelty_impact_=1, pipeline_name_=None):
        """Create pipeline and add each element to its dict. Start pipeline afterwards.

        Parameters:
        ip_ (mandatory, string): IP of target host.
        port_ (mandatory, int): Port of target host.
        topic_ (mandatory, string): Name of topic that data should be published on.
        frequency_ (mandatory, float): Frequency (in Hz) in that the data will be published on the given topic_.
        channel_name_ (mandatory, string): Name of the new channel.
        channel_limits_ (optional, list of floats): The lower/upper limits of the 'normal-behaving' data.
        channel_frequency_ (optional, float): Frequency (in Hz) in that the data will repeat itself.
        novelty_frequency_ (optional, float): Frequency (in Hz) in that the novelty will appear.
        novelty_duration_ (optional, float): The duration in seconds that the novelty will appear.
        novelty_impact_ (optional, float): Scaling factor of the noise that will be produced during the novelty appearance.
        pipeline_name_ (optional, str): Name that a certain pipeline can later be associated with.
        """
        # add host
        host_id = self._add_connection(ip_, port_)
        # add topic
        topic_id = self._add_topic(topic_, frequency_)
        # add channel
        channel_id = self._add_channel(channel_name_, channel_limits_, channel_frequency_)
        # add novelty
        novelty_id = self._add_novelty(novelty_frequency_, novelty_duration_, novelty_impact_)
        # add everything to pipeline
        pipeline_id = self._add_pipeline(pipeline_name_, host_id, topic_id, channel_id, novelty_id)
        # init and assign generator for each new pipeline
        self._add_handlers(pipeline_id)
        # add new job in scheduler
        self.Scheduler.add_job(func=self.publish_data, trigger='interval', seconds=(1/frequency_), kwargs={'id_':pipeline_id})

    def publish_data(self, id_):
        """Get data and publish it to target host.

        Parameters:
        id_ (mandatory, int): ID of pipeline.
        """
        # get topic, channelname and data in json format
        topic = self.topics[id_]['topic']
        jdata = self.handlers[id_]['generator'].get_payload()
        # publish data via client
        ret = self.handlers[id_]['mqtt'].publish(topic, jdata)
    
    def _add_handlers(self, id_):
        """Initializes instance of Generator, Clients, etc.. Pass these instances to their corresponding dicts.

        Parameters:
        id_ (mandatory, int): ID of pipeline.
        
        Note:
        - ID in handlers dict will always be the same as the pipeline ID.
        """
        # use given pipeline_id to get ids of other dicts.
        tid = self.pipelines[id_]['topic_id']
        cid = self.pipelines[id_]['channel_id']
        nid = self.pipelines[id_]['novelty_id']
        # gather required information from specific dicts and feed them to Generator instance.
        gen = Generator(
            channel_name_=self.channels[cid]['name'],
            channel_limits_=self.channels[cid]['limits'], 
            channel_frequency_=self.channels[cid]['frequency'], 
            novelty_frequency_=self.novelties[nid]['frequency'],
            novelty_duration_=self.novelties[nid]['duration'],
            novelty_impact_=self.novelties[nid]['impact']
            )        
        # init mqtt client
        client = mqtt.Client()
        # connect to server
        client.connect(self.connections[id_]['ip'], self.connections[id_]['port'])

        # init subdict
        self.handlers[id_] = {}
        # assign generator to handlers dict
        self.handlers[id_]['generator'] = gen
        self.handlers[id_]['mqtt'] = client

    def _add_pipeline(self, name_, host_id_, topic_id_, channel_id_, novelty_id_):
        """Adding a new entry in the pipeline dictionary.
        
        Parameters:
        name_ (mandatory, str): Name of the new pipeline.
        host_id_ (mandatory, int): ID of host in host dictionary.
        topic_id_ (mandatory, int): ID of topic in topic dictionary.
        channel_id_ (mandatory, int): ID of channel in channel dictionary.
        novelty_id_ (mandatory, int): ID of novelty in novelty dictionary.

        Note:
        - name_ can also be None or an empty string.
        """
        # get id of next key in pipeline dict
        id = len(self.pipelines.keys())
        # add entries to dict
        self.pipelines[id] = {
            'name':name_,
            'host_id':host_id_,
            'topic_id':topic_id_,
            'channel_id':channel_id_,
            'novelty_id':novelty_id_,
            'active':1
        }
        # return the id that has just been added
        return id

    def _add_connection(self, ip_, port_):
        """Add connection to dict of connections.
        
        Parameters:
        ip_ (mandatory, string): IP of target host.
        port_ (mandatory, int): Port of target host.
        """
        # get id of next connection
        id = len(self.connections.keys())
        # add connection to dict
        self.connections[id] = {
            'ip':ip_,
            'port':port_
        }
        # return the id that has just been added
        return id

    def _add_topic(self, topic_, frequency_):
        """Add topic to dict of topics.

        Parameters:
        topic_ (mandatory, string): Name of topic that data should be published on.
        frequency_ (mandatory, float): Frequency (in Hz) in that the data will be published on the given topic_.
        """
        # get id of next entry in topics dict
        id = len(self.topics.keys())
        # add entry to dict
        self.topics[id] = {
            'topic':topic_,
            'frequency':frequency_
        }
        # return the id that has just been added
        return id

    def _add_channel(self, name_, limits_=[-1, 1], frequency_=0.2):
        """Add channel to dict of channels.

        Parameters:
        name_ (mandatory, string): Name of the new channel.
        limits_ (optional, list of floats): The lower/upper limits of the 'normal-behaving' data.
        frequency_ (optional, float): Frequency (in Hertz) in that the data will repeat itself.
        """
        # get id of next entry in channels dict
        id = len(self.channels.keys())
        # add entry to dict
        self.channels[id] = {
            'name':name_,
            'limits':limits_,
            'frequency':frequency_
        }
        # return the id that has just been added
        return id

    def _add_novelty(self, frequency_=0.0167, duration_=5, impact_=1):
        """Add novelty to dict of novelties.

        Parameters:
        frequency_ (optional, float): Frequency (in Hz) in that the novelty will appear.
        duration_ (optional, float): The duration in seconds that the novelty will appear.
        impact_ (optional, float): Scaling factor of the noise that will be produced during the novelty appearance.

        Note:
        - A novelty is a random noise that will interfere with the original 'normal-behaving' signal.
        - If the duration is equal or greater than the frequency, the influence of the novelty will stay permanently.
        """
        # get id of next entry in novelty dict
        id = len(self.novelties.keys())
        # add entry to dict
        self.novelties[id] = {
            'frequency':frequency_,
            'duration':duration_,
            'impact':impact_
        }
        # return the id that has just been added
        return id

    def switch_pipeline(self, id_):
        """Turn on/off a pipeline.

        Parameters:
        id_ (mandatory, int): ID of the pipeline in the pipeline dict.
        """
        # switch the active state
        self.pipelines[id_]['active'] = 1 - self.pipelines[id_]['active']
        # adjust current state of job accordingly.
        if (self.pipelines[id_]['active'] == 1):
            # TODO: start job
            pass
        else:
            pass
            # TODO: stop job
