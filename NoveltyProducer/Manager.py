#!/usr/bin/env python3

from NoveltyProducer.Technican import Technican
from NoveltyProducer.Generator import Generator
from apscheduler.schedulers.background import BackgroundScheduler
from re import search as research
import paho.mqtt.client as mqtt

class InvalidInputTypeError(Exception):
    """The InvalidInputTypeError is raised whenever a specific input of a specific function has an invalid/unexpected type."""
    pass

class InvalidInputValueError(Exception):
    """The InvalidInputValueError is raised whenever a specific input of a specific function has an invalid/unexpected value."""
    pass
    
class OnConnectError(Exception):
    """The OnConnectError is raised whenever the connection to a target system failed."""
    pass

    
class Manager:
    """
    Class to connect to a given host and send data with a given frequency.
    """
    
    # set default init arguments
    defaults = {}
    defaults['channel_limits'] = [-1, 1]
    defaults['channel_frequency'] = 0.1
    defaults['pipeline_name'] = 'Pipe'
        
    def __init__(self, verbose_=False):
        # init handlers
        self.Scheduler = BackgroundScheduler()
        # start scheduler
        self.Scheduler.start()        
        # init dict for handlers, pipelines, connections, topics and channels
        self.handlers = {} # contains instances of Generator
        self.pipelines = {} # contains ids of host, topic, ...
        self.connections = {} # contains host informations
        self.topics = {} # contains topic informations
        self.channels = {} # contains channel informations
        
        # init parameters
        self.verbose = verbose_

    def create_pipeline(self, ip_, port_, topic_, frequency_, channel_name_, \
        channel_limits_=defaults['channel_limits'], channel_frequency_=defaults['channel_frequency'], pipeline_name_=defaults['pipeline_name']):
        """Create pipeline and add each element to its dict. Start pipeline afterwards.

        Parameters:
        ip_ (mandatory, string): IP of target host.
        port_ (mandatory, int): Port of target host.
        topic_ (mandatory, string): Name of topic that data should be published on.
        frequency_ (mandatory, float): Frequency (in Hz) in that the data will be published on the given topic_.
        channel_name_ (mandatory, string): Name of the new channel.
        channel_limits_ (optional, list of floats): The lower/upper limits of the data.
        channel_frequency_ (optional, float): Frequency (in Hz) in that the data will repeat itself.
        pipeline_name_ (optional, str): Name that a certain pipeline can later be associated with.
        """
        # check inputs
        self._check_pipeline_materials(ip_, port_, topic_, frequency_, channel_name_, channel_limits_, channel_frequency_, pipeline_name_)
        # add host
        host_id = self._add_connection(ip_, port_)
        # add topic
        topic_id = self._add_topic(topic_, frequency_)
        # add channel
        channel_id = self._add_channel(channel_name_, channel_limits_, channel_frequency_)
        # add everything to pipeline
        pipeline_id = self._add_pipeline(pipeline_name_, host_id, topic_id, channel_id)
        # init and assign generator for each new pipeline
        self._add_handlers(pipeline_id)
        # add new job in scheduler
        self.Scheduler.add_job(func=self.publish_data, trigger='interval', seconds=(1/frequency_), id=str(pipeline_id), kwargs={'id_':pipeline_id})

    def add_channel_to_pipeline(self, id_, name_, limits_=defaults['channel_limits'], frequency_=defaults['channel_frequency']):
        """Add another channel to an already existing pipeline.
        
        Parameters:
        id_ (mandatory, int): ID of pipeline.
        name_ (mandatory, string): Name of channel.
        limits_ (optional, list of floats): The lower/upper limits of the data.
        frequency_ (optional, float): Frequency (in Hz) in that the data will repeat itself.
        """
        # add channel
        cid = self._add_channel(name_=name_, limits_=limits_, frequency_=frequency_)
        # add channel to target pipeline
        self.pipelines[id_]['channel_id'].append(cid)
        # get new generator and pass it to technican
        self._update_technican(id_, cid)

    def publish_data(self, id_):
        """Get data and publish it to target host.

        Parameters:
        id_ (mandatory, int): ID of pipeline.
        """
        # get topic, channelname and data in json format
        topic = self.topics[id_]['topic']
        jdata = self.handlers[id_]['technican'].get_payload()
        # publish data via client
        ret = self.handlers[id_]['mqtt'].publish(topic, jdata)
    
    def _update_technican(self, pid_, cid_):
        """Initialize instance of new Generator and pass it to technican.
        
        Parameters:
        pid_ (mandatory, int): Pipeline id.
        cid_ (mandatory, int): Channel id.
        """
        
        # create new generator
        gen = Generator(
            name_=self.channels[cid_]['name'],
            limits_=self.channels[cid_]['limits'], 
            frequency_=self.channels[cid_]['frequency']
        )
        
        # get corresponding technican
        techie = self.handlers[pid_]['technican']
        
        # add generator to his dict of generators
        techie.generators[cid_] = gen

    
    def _add_handlers(self, id_):
        """Initializes instance of Generator, Clients, etc.. Pass these instances to their corresponding dicts.

        Parameters:
        id_ (mandatory, int): ID of pipeline.
        
        Note:
        - ID in handlers dict will always be the same as the pipeline ID.
        """
        # use given pipeline_id to get ids of channels.
        cids = self.pipelines[id_]['channel_id']
        
        # create list to keep track of generators bought.
        gens = {}
        # loop over each given channel and get a generator for each.
        for cid in cids:
            # buy single generator
            gen = Generator(
                name_=self.channels[cid]['name'],
                limits_=self.channels[cid]['limits'], 
                frequency_=self.channels[cid]['frequency']
                ) 
            # append to list of generators
            gens[cid] = gen
            
        # hire technican to get all generators working.
        techie = Technican(gens)
            
        # init mqtt client
        client = mqtt.Client()
        # connect to server
        try:
            client.connect(self.connections[id_]['ip'], self.connections[id_]['port'], 60)
        except Exception as err:
            raise OnConnectError("Failed to establish connection to %s:%i - %s" % (self.connections[id_]['ip'], self.connections[id_]['port'], err))

        # init subdict
        self.handlers[id_] = {}
        # assign techie to handlers dict
        self.handlers[id_]['technican'] = techie
        self.handlers[id_]['mqtt'] = client

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

    def _add_channel(self, name_, limits_=defaults['channel_limits'], frequency_=defaults['channel_frequency']):
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

    def _add_pipeline(self, name_, host_id_, topic_id_, channel_id_):
        """Adding a new entry in the pipeline dictionary.
        
        Parameters:
        name_ (mandatory, str): Name of the new pipeline.
        host_id_ (mandatory, int): ID of host in host dictionary.
        topic_id_ (mandatory, int): ID of topic in topic dictionary.
        channel_id_ (mandatory, int): ID of channel in channel dictionary.

        Note:
        - name_ can also be None or an empty string.
        """
        # get all pipeline names.
        pipeline_names = [v['name'] for k,v in self.pipelines.items()]
        # new pipeline name already given?
        if name_ in pipeline_names:
            # get new unique name
            name = self._get_unique_name(pipeline_names, name_)
        else:
            # new name is unique
            name = name_
        
        # get id of next key in pipeline dict
        id = len(self.pipelines.keys())
        # add entries to dict
        self.pipelines[id] = {
            'name':name,
            'host_id':host_id_,
            'topic_id':topic_id_,
            'channel_id':[channel_id_],
            'active':1
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
            # resume job
            self.Scheduler.get_job(str(id_)).resume()
        else:
            # pause job
            self.Scheduler.get_job(str(id_)).pause()

    def _get_unique_name(self, names_, name_):
        """Find a new name for name_ so that it is unique in the list of names_.

        Parameters:
        names_ (mandatory, list of strings): List of names that are already in use.
        name_ (mandatory, string): Name that should be unique to names_.
        """
        # set name to start with.
        name = name_
        # loop until name is unique.
        while name in names_:
            name = self._count_up(name)
        
        # return unique name
        return name
        
    def _count_up(self, name_, suffix_='_'):
        """Search for pattern in name_. Add that pattern if not found or add +1 to existing pattern.
        
        Parameters:
        name_ (mandatory, string): Name that should be unique to names_.
        suffix_ (optional, string): Will be attached to very end of name_.
        """
        # search for suffix and numbers at the very end of name.
        search = research(r'[' + suffix_ + r']([0-9]+)$', name_)
        # found something?
        if search:
            # what number was found?
            num = int(search.group(0)[1:])
            # add +1 to that number.
            name = name_[:-len(search.group(0))] + suffix_ + str(num+1)
        else:
            # attach suffix
            name = name_ + suffix_ + '0'
        
        return name
        
    def _check_pipeline_materials(self, ip_, port_, topic_, frequency_, channel_name_, channel_limits_, channel_frequency_, pipeline_name_):
        """Check all inputs that are used to create a pipeline"""
        # ip_
        if not isinstance(ip_, str):
            raise InvalidInputTypeError("Content of ip_ is type %s but should be a of type string." % type(ip_))
            
        # port_
        if not isinstance(port_, int):
            raise InvalidInputTypeError("Content of port_ is type %s but should be a of type int." % type(port_))
        if ((port_ < 0) | (port_ > 65535)):
            raise InvalidInputValueError("Value of port_ (%s) is not in valid port range (0 - 65535)." % str(port_))

        # topic_
        if not isinstance(topic_, str):
            raise InvalidInputTypeError("Content of topic_ is type %s but should be a of type string." % type(topic_))
            
        # frequency_
        if not isinstance(frequency_, (int, float)):
            raise InvalidInputTypeError("Content of frequency_ is type %s but should be a of type int or float." % type(frequency_))
        if frequency_ <= 0:
            raise InvalidInputValueError("Value of frequency_ (%s [Hz]) is negative or zero but should be positive." % str(frequency_))
            
        # channel_name_
        if not isinstance(channel_name_, str):
            raise InvalidInputTypeError("Content of channel_name_ is type %s but should be a of type string." % type(channel_name_))
            
        # channel_limits_
        if not isinstance(channel_limits_, list):
            raise InvalidInputTypeError("Content of channel_limits_ is type %s but should be a of type list." % type(channel_limits_))
        if not all(isinstance(x, (int, float)) for x in channel_limits_):
            raise InvalidInputValueError("Not all values of channel_limits_ are of type int or float.")
            
        # channel_frequency_
        if not isinstance(channel_frequency_, (int, float)):
            raise InvalidInputTypeError("Content of channel_frequency_ is type %s but should be a of type int or float." % type(channel_frequency_))
        if channel_frequency_ <= 0:
            raise InvalidInputValueError("Value of channel_frequency_ (%s [Hz]) is negative or zero but should be positive." % str(channel_frequency_))
            
        # pipeline_name_
        if not isinstance(pipeline_name_, str):
            raise InvalidInputTypeError("Content of pipeline_name_ is type %s but should be a of type string." % type(pipeline_name_))