#!/usr/bin/env python3

# import own libs
from transmitter.engine import Technician
from transmitter.engine import Generator
from transmitter.auxiliary.constants import DEFAULT_PIPELINE_SETTINGS
from transmitter.auxiliary.exceptions import (
    InvalidInputTypeError,
    InvalidInputValueError,
    OnConnectError,
)

# import native libs
from re import search as research

# import 3rd party libs
from apscheduler.schedulers.background import BackgroundScheduler
import paho.mqtt.client as mqtt

"""Use this module to manage the complete mqtt process and all the other engine parts."""


class Manager:
    """
    Class to connect to a given host and send data with a given frequency.
    """

    # set default values
    defaults = DEFAULT_PIPELINE_SETTINGS

    def __init__(self, verbose_=False):
        """Initialize variables"""
        # init handlers
        self.Scheduler = BackgroundScheduler()
        # start scheduler
        self.Scheduler.start()        
        # init dict for handlers, pipelines, connections, topics and channels
        self.handlers = {}  # contains instances of Generator
        self.pipelines = {}  # contains ids of host, topic, ...
        self.connections = {}  # contains host information
        self.topics = {}  # contains topic information
        self.channels = {}  # contains channel information
        
        # init parameters
        self.verbose = verbose_

    def create_pipeline(self, ip_, port_, topic_, frequency_, pipeline_name_=defaults['pipeline_name']):
        """Create pipeline and add each element to its dict. Start pipeline afterwards.

        Parameters:
        ip_ (mandatory, string): IP of target host.
        port_ (mandatory, int): Port of target host.
        topic_ (mandatory, string): Name of topic that data should be published on.
        frequency_ (mandatory, float): Frequency (in Hz) in that the data will be published on the given topic_.
        """
        # check inputs
        self._check_inputs(ip_=ip_, port_=port_, topic_=topic_, frequency_=frequency_, pipeline_name_=pipeline_name_)
        # add host
        host_id = self._add_connection(ip_, port_)
        # add topic
        topic_id = self._add_topic(topic_, frequency_)
        # add everything to pipeline
        pipeline_id = self._add_pipeline(pipeline_name_, host_id, topic_id)
        # init and assign generator for each new pipeline
        self._add_handlers(pipeline_id)
        # add new job in scheduler
        self.Scheduler.add_job(func=self.publish_data, trigger='interval', seconds=(1/frequency_),
                               id=str(pipeline_id), kwargs={'pid_':pipeline_id})
        # pause job since no channel is yet on pipeline
        self.Scheduler.get_job(str(pipeline_id)).pause()
        # return id of pipeline that has just been created
        return pipeline_id

    def add_function(self, pid_, channel_name_, limits_=defaults['channel_limits'],
                     frequency_=defaults['channel_frequency'], type_=defaults['channel_type'],
                     dead_frequency_=defaults['dead_frequency'], dead_period_=defaults['dead_period']):
        """Add a function to an already existing pipeline.
        
        Parameters:
        :param pid_: (mandatory, int) ID of pipeline.
        :param channel_name_: (mandatory, string) Name of channel.
        :param limits_: (optional, list of floats) The lower/upper limits of the data.
        :param frequency_: (optional, float) Frequency (in Hz) in that the data will repeat itself.
        :param type_: (optional, string) Defines kind of function that will be added (e.g. sine wave).
        :param dead_frequency_: (optional, float) Frequency (in Hz) in that the function will return zero.
        :param dead_period_: (optional, float) Duration in that the output will stay zero.
        """
        # check inputs
        self._check_inputs(channel_name_=channel_name_, channel_limits_=limits_, channel_frequency_=frequency_,
                           channel_type_=type_, dead_frequency_=dead_frequency_, dead_period_=dead_period_)
        # add channel
        cid = self._add_channel(name_=channel_name_, limits_=limits_, frequency_=frequency_, type_=type_,
                                dead_frequency_=dead_frequency_, dead_period_=dead_period_)
        # add channel to target pipeline
        self.pipelines[pid_]['channel_id'].append(cid)
        # is pipeline currently inactive?
        if self.pipelines[pid_]['active'] == 0:
            # switch pipeline on
            self.switch_pipeline(pid_)
        # get new generator and pass it to Technician
        self._update_technician(pid_)
        # return id of channel that has just been added
        return cid

    def add_replay(self, pid_, data_, name_):
        """Add an dataset that will be replayed.
        
        Parameters:
        :param pid_: (mandatory, int) ID of pipeline.
        :param data_: (mandatory, list) Data to replay.
        :param name_: (mandatory, string) Name of channel.
        """
        # check inputs
        self._check_inputs(replay_data_=data_, channel_name_=name_)
        # get topic frequency
        frequency = self.topics[pid_]['frequency']
        # add channel
        cid = self._add_channel(name_=name_, frequency_=frequency, type_='replay', replay_data_=data_)
        # add channel to target pipeline
        self.pipelines[pid_]['channel_id'].append(cid)
        # is pipeline currently inactive?
        if self.pipelines[pid_]['active'] == 0:
            # switch pipeline on
            self.switch_pipeline(pid_)
        # get new generator and pass it to Technician
        self._update_technician(pid_)
        # return ids of channels that has just been added
        return cid

    def remove_channel(self, cid_):
        """Remove existing channel from each pipeline.
        
        Parameters:
        cid_ (mandatory, int): ID of channel.
        """
        # remove channel from channel dict
        self.channels.pop(cid_)
        # loop each pipeline
        for pid in self.pipelines:
            # is channel id in pipeline?
            if cid_ in self.pipelines[pid]['channel_id']:
                # remove it.
                self.pipelines[pid]['channel_id'].remove(cid_)
                # no channels left on pipeline?
                if len(self.pipelines[pid]['channel_id']) == 0:
                    # switch pipeline to inactive
                    self.switch_pipeline(pid)
                # call corresponding Technician.
                self._update_technician(pid)
                
    def publish_data(self, pid_):
        """Get data and publish it to target host.

        Parameters:
        pid_ (mandatory, int): ID of pipeline.
        """
        # get topic, channelname and data in json format
        topic = self.topics[pid_]['topic']
        jdata = self.handlers[pid_]['technician'].get_payload()
        # publish data via client
        ret = self.handlers[pid_]['mqtt'].publish(topic, jdata)
        
        return ret
    
    def _update_technician(self, pid_):
        """Get list of installed generators from technician. Compare with desired list. Take action if necessary.
        
        Parameters:
        pid_ (mandatory, int): Pipeline id.
        """
        # get corresponding technician
        techie = self.handlers[pid_]['technician']
        
        # get keys (channel ids) of generators
        installed_generators = [key for key, gen in techie.generators.items()]
        desired_generators = self.pipelines[pid_]['channel_id']
        
        # compare with current channel ids
        todos = [g for g in installed_generators + desired_generators
                 if g not in installed_generators or g not in desired_generators]
        
        # anything to do?
        for todo in todos:
            # install new generators?
            if todo in desired_generators:
                self._add_generator(pid_, todo)
            # remove installed generator?
            elif todo in installed_generators:
                self._remove_generator(pid_, todo)
        
    def _add_generator(self, pid_, cid_):
        """Init new generator and update list of corresponding technician.
        
        Parameters:
        pid_ (mandatory, int): Pipeline id.
        cid_ (mandatory, int): Channel id.
        """
        # get corresponding technician
        techie = self.handlers[pid_]['technician']
        
        # create new generator
        gen = Generator(
            name_=self.channels[cid_]['name'],
            limits_=self.channels[cid_]['limits'], 
            frequency_=self.channels[cid_]['frequency'],
            type_=self.channels[cid_]['type'],
            dead_frequency_=self.channels[cid_]['dead_frequency'],
            dead_period_=self.channels[cid_]['dead_period'],
            replay_data_=self.channels[cid_]['replay_data']
        )
        
        # add generator to his dict of generators
        techie.generators[cid_] = gen
        
    def _remove_generator(self, pid_, cid_):
        """Remove old generator and update list of corresponding technician.
        
        Parameters:
        pid_ (mandatory, int): Pipeline id.
        cid_ (mandatory, int): Channel id.
        """
        # get corresponding technician
        techie = self.handlers[pid_]['technician']
        # remove old generator from dict of generators
        techie.generators.pop(cid_)
        
    def _add_handlers(self, id_):
        """Initializes instance of Generator, Clients, etc.. Pass these instances to their corresponding dicts.

        Parameters:
        id_ (mandatory, int): ID of pipeline.
        
        Note:
        - ID in handlers dict will always be the same as the pipeline ID.
        """
            
        # hire technician
        techie = Technician({})
            
        # init mqtt client
        client = mqtt.Client()
        # connect to server
        try:
            client.connect(self.connections[id_]['ip'], self.connections[id_]['port'], 60)
        except Exception as err:
            raise OnConnectError("Failed to establish connection to %s:%i - %s" %
                                 (self.connections[id_]['ip'], self.connections[id_]['port'], err))

        # init sub-dict
        self.handlers[id_] = {}
        # assign techie to handlers dict
        self.handlers[id_]['technician'] = techie
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
            'ip': ip_,
            'port': port_
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
            'topic': topic_,
            'frequency': frequency_
        }
        # return the id that has just been added
        return id

    def _add_channel(self, name_, limits_=defaults['channel_limits'], frequency_=defaults['channel_frequency'],
                     type_=defaults['channel_type'], dead_frequency_=defaults['dead_frequency'],
                     dead_period_=defaults['dead_period'], replay_data_=defaults['replay_data']):
        """Add channel to dict of channels.

        Parameters:
        name_ (mandatory, string): Name of the new channel.
        limits_ (optional, list of floats): The lower/upper limits of the data.
        frequency_ (optional, float): Frequency (in Hertz) in that the data will repeat itself.
        """
        # get id of next entry in channels dict
        id = 0 if len(self.channels.keys()) == 0 else max(self.channels.keys()) + 1
        # add entry to dict
        self.channels[id] = {
            'name': name_,
            'limits': limits_,
            'frequency': frequency_,
            'type': type_,
            'dead_frequency': dead_frequency_,
            'dead_period': dead_period_,
            'replay_data': replay_data_
            }
        # return the id that has just been added
        return id

    def _add_pipeline(self, name_, host_id_, topic_id_):
        """Adding a new entry in the pipeline dictionary.
        
        Parameters:
        name_ (mandatory, str): Name of the new pipeline.
        host_id_ (mandatory, int): ID of host in host dictionary.
        topic_id_ (mandatory, int): ID of topic in topic dictionary.

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
            'channel_id':[],
            'active':0
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
        if self.pipelines[id_]['active'] == 1:
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

    @staticmethod
    def _count_up(name_, suffix_='_'):
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

    @staticmethod
    def _check_inputs(**kwargs):
        """Check all inputs that are used to create a pipeline"""
        # ip_
        if 'ip_' in kwargs:
            if not isinstance(kwargs['ip_'], str):
                raise InvalidInputTypeError("Content of ip_ is type %s but should be a of type string." %
                                            type(kwargs['ip_']))

        # port_
        if 'port_' in kwargs:
            if not isinstance(kwargs['port_'], int):
                raise InvalidInputTypeError("Content of port_ is type %s but should be a of type int." %
                                            type(kwargs['port_']))
            if (kwargs['port_'] < 0) | (kwargs['port_'] > 65535):
                raise InvalidInputValueError("Value of port_ (%s) is not in valid port range (0 - 65535)." %
                                             str(kwargs['port_']))

        # topic_
        if 'topic_' in kwargs:
            if not isinstance(kwargs['topic_'], str):
                raise InvalidInputTypeError("Content of topic_ is type %s but should be a of type string." %
                                            type(kwargs['topic_']))

        # frequency_
        if 'frequency_' in kwargs:
            if not isinstance(kwargs['frequency_'], (int, float)):
                raise InvalidInputTypeError("Content of frequency_ is type %s but should be a of type int or float." %
                                            type(kwargs['frequency_']))
            if kwargs['frequency_'] <= 0:
                raise InvalidInputValueError("Value of frequency_ (%s [Hz]) is negative "
                                             "or zero but should be positive." % str(kwargs['frequency_']))
            
        # channel_name_
        if 'channel_name_' in kwargs:
            if not isinstance(kwargs['channel_name_'], str):
                raise InvalidInputTypeError("Content of channel_name_ is type %s but should be a of type string." %
                                            type(kwargs['channel_name_']))
            
        # channel_limits_
        if 'channel_limits_' in kwargs:
            if kwargs['channel_limits_']:
                if not isinstance(kwargs['channel_limits_'], list):
                    raise InvalidInputTypeError("Content of channel_limits_ is type %s but should be a of type list." %
                                                type(kwargs['channel_limits_']))
                if not all(isinstance(x, (int, float)) for x in kwargs['channel_limits_']):
                    raise InvalidInputValueError("Not all values of channel_limits_ are of type int or float.")
            
        # channel_frequency_
        if 'channel_frequency_' in kwargs:
            if not isinstance(kwargs['channel_frequency_'], (int, float)):
                raise InvalidInputTypeError("Content of channel_frequency_ is type %s but should "
                                            "be a of type int or float." % type(kwargs['channel_frequency_']))
            if kwargs['channel_frequency_'] <= 0:
                raise InvalidInputValueError("Value of channel_frequency_ (%s [Hz]) is negative or zero but"
                                             " should be positive." % str(kwargs['channel_frequency_']))
            
        # channel_type_
        if 'channel_type_' in kwargs:
            if not isinstance(kwargs['channel_type_'], str):
                raise InvalidInputTypeError("Content of channel_type_ is type %s but should be a of type string." %
                                            type(kwargs['channel_type_']))
            
        # pipeline_name_
        if 'pipeline_name_' in kwargs:
            if not isinstance(kwargs['pipeline_name_'], str):
                raise InvalidInputTypeError("Content of pipeline_name_ is type %s but should be a of type string." %
                                            type(kwargs['pipeline_name_']))
            
        # dead_frequency_
        if 'dead_frequency_' in kwargs:
            if not isinstance(kwargs['dead_frequency_'], (int, float)):
                raise InvalidInputTypeError("Content of dead_frequency_ is type %s but should "
                                            "be a of type int or float." % type(kwargs['dead_frequency_']))
            if kwargs['dead_frequency_'] <= 0:
                raise InvalidInputValueError("Value of dead_frequency_ (%s [Hz]) is negative or "
                                             "zero but should be positive." % str(kwargs['dead_frequency_']))
            
        # dead_period_
        if 'dead_period_' in kwargs:
            if not isinstance(kwargs['dead_period_'], (int, float)):
                raise InvalidInputTypeError("Content of dead_period_ is type %s but "
                                            "should be a of type int or float." % type(kwargs['dead_period_']))
            if kwargs['dead_period_'] < 0:
                raise InvalidInputValueError("Value of dead_period_ (%s [Hz]) is "
                                             "negative but should be zero or positive." % str(kwargs['dead_period_']))
        
        # replay_data_
        if 'replay_data_' in kwargs:
            if not isinstance(kwargs['replay_data_'], list):
                raise InvalidInputTypeError("Content of replay_data_ is "
                                            "type %s but should be an list." % type(kwargs['replay_data']))
