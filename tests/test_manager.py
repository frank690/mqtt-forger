import copy
import numpy as np
import paho.mqtt.client as mqtt
from unittest import TestCase
from NoveltyProducer.Manager import Manager, InvalidInputTypeError, InvalidInputValueError
from NoveltyProducer.Generator import Generator
from apscheduler.job import Job

ip = 'test.mosquitto.org'
# ip = 'localhost' 
port = 1883
topic = 'foo'
frequency = 1
channel_name = 'bar'
channel_limits = [-2, 2]
channel_frequency = 0.1
novelty_frequency = 0.01
novelty_duration = 1
novelty_impact = 1
pipeline_name = 'pipe'

class TestBaseUnit(TestCase):

    def test_value_output(self):
        """Test output of each function."""
        
        # init instance of Manager
        man = Manager()
        
        # _add_connection
        con_id = man._add_connection(ip_=ip, port_=port)
        self.assertEqual(ip, man.connections[con_id]['ip'])
        self.assertEqual(port, man.connections[con_id]['port'])
        
        # _add_topic
        top_id = man._add_topic(topic_=topic, frequency_=frequency)
        self.assertEqual(topic, man.topics[top_id]['topic'])
        self.assertEqual(frequency, man.topics[top_id]['frequency'])
        
        # _add_channel
        chn_id = man._add_channel(name_=channel_name, limits_=channel_limits, frequency_=channel_frequency)
        self.assertEqual(channel_name, man.channels[chn_id]['name'])
        self.assertEqual(channel_limits, man.channels[chn_id]['limits'])
        self.assertEqual(channel_frequency, man.channels[chn_id]['frequency'])
        
        # _add_novelty
        nov_id = man._add_novelty(frequency_=novelty_frequency, duration_=novelty_duration, impact_=novelty_impact)
        self.assertEqual(novelty_frequency, man.novelties[nov_id]['frequency'])
        self.assertEqual(novelty_duration, man.novelties[nov_id]['duration'])
        self.assertEqual(novelty_impact, man.novelties[nov_id]['impact'])
        
        # _add_pipeline
        pipe_id = man._add_pipeline(name_=pipeline_name, host_id_=con_id, topic_id_=top_id, channel_id_=chn_id, novelty_id_=nov_id)
        self.assertEqual(pipeline_name, man.pipelines[pipe_id]['name'])
        self.assertEqual(con_id, man.pipelines[pipe_id]['host_id'])
        self.assertEqual(top_id, man.pipelines[pipe_id]['topic_id'])
        self.assertEqual(chn_id, man.pipelines[pipe_id]['channel_id'])
        self.assertEqual(nov_id, man.pipelines[pipe_id]['novelty_id'])
        self.assertEqual(1, man.pipelines[pipe_id]['active'])
        
        # switch_pipeline (on to off)
        pipeline_status = man.pipelines[pipe_id]['active']
        man.switch_pipeline(pipe_id)
        self.assertTrue(pipeline_status != man.pipelines[pipe_id]['active'])
        
        # switch_pipeline (off to on)
        pipeline_status = man.pipelines[pipe_id]['active']
        man.switch_pipeline(pipe_id)
        self.assertTrue(pipeline_status != man.pipelines[pipe_id]['active'])
        
    def test_type_output(self):
        """Test types of output"""
        
        # init instance of Manager
        man = Manager()
        
        # _add_connection
        con_id = man._add_connection(ip_=ip, port_=port)
        self.assertIsInstance(con_id, int)
        
        # _add_topic
        top_id = man._add_topic(topic_=topic, frequency_=frequency)
        self.assertIsInstance(top_id, int)
        
        # _add_channel
        chn_id = man._add_channel(name_=channel_name, limits_=channel_limits, frequency_=channel_frequency)
        self.assertIsInstance(chn_id, int)
        
        # _add_novelty
        nov_id = man._add_novelty(frequency_=novelty_frequency, duration_=novelty_duration, impact_=novelty_impact)
        self.assertIsInstance(nov_id, int)
        
        # _add_pipeline
        pipe_id = man._add_pipeline(name_='pipe', host_id_=con_id, topic_id_=top_id, channel_id_=chn_id, novelty_id_=nov_id)
        self.assertIsInstance(pipe_id, int)
        
        # _add_handlers
        man._add_handlers(pipe_id)
        self.assertIsInstance(man.handlers[pipe_id]['generator'], Generator)
        self.assertIsInstance(man.handlers[pipe_id]['mqtt'], mqtt.Client)
        
        # create_pipeline
        man.create_pipeline(ip_=ip, port_=port, topic_=topic, channel_frequency_=channel_frequency, channel_name_=channel_name, pipeline_name_='sffresch')
        pipe_id = str([k for k,v in man.pipelines.items() if man.pipelines[k]['name'] == 'sffresch'][0])
        self.assertIsInstance(man.Scheduler.get_job(pipe_id), Job)

    def test_invalid_inputs(self):
        """Test for all expected errors that should be raised when given invalid inputs"""
        
        # init instance of Manager
        man = Manager()
        
        # ip_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=127001, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name)
        
        # port_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_='1883', topic_=topic, frequency_=frequency, channel_name_=channel_name)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=65536, topic_=topic, frequency_=frequency, channel_name_=channel_name)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=-1, topic_=topic, frequency_=frequency, channel_name_=channel_name)
            
        # topic_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=42, frequency_=frequency, channel_name_=channel_name)

        # frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_='1', channel_name_=channel_name)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=0, channel_name_=channel_name)
            
        # channel_name_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=42)

        # channel_limits_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, channel_limits_=42)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, channel_limits_=['-12.3', 13.5])
            
        # channel_frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, channel_frequency_='42')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, channel_frequency_=0)

        # novelty_frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, novelty_frequency_='42')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, novelty_frequency_=0)
            
        # novelty_duration_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, novelty_duration_='42')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, novelty_duration_=-42)
            
        # novelty_impact_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, novelty_impact_='42')

        # channel_name_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=ip, port_=port, topic_=topic, frequency_=frequency, channel_name_=channel_name, pipeline_name_=42)