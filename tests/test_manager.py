import copy
import numpy as np
from unittest import TestCase
from NoveltyProducer.Manager import Manager

class TestBaseUnit(TestCase):

    def test_type_output(self):
        """Test types of output"""
        
        # init instance of Manager
        man = Manager()
        
        # _add_connection
        con_id = man._add_connection(ip_='localhost', port_=1883)
        self.assertTrue(isinstance(con_id, int)) 
        
        # _add_topic
        top_id = man._add_topic(topic_='foo', frequency_=1)
        self.assertTrue(isinstance(top_id, int)) 
        
        # _add_channel
        chn_id = man._add_channel(channel_name_='bar', channel_limits_=[-1, 1], channel_frequency_=0.1)
        self.assertTrue(isinstance(chn_id, int))
        
        # _add_novelty
        nov_id = man._add_novelty(novelty_frequency_=0.01, novelty_duration_=1, novelty_impact_=1)
        self.assertTrue(isinstance(nov_id, int))
        
        # _add_pipeline
        pipe_id = man._add_pipeline(pipeline_name_='pipe', host_id=con_id, topic_id=top_id, channel_id=chn_id, novelty_id=nov_id)
        self.assertTrue(isinstance(pipe_id, int))

    def test_invalid_inputs(self):
        """Test for all expected errors that should be raised when given invalid inputs"""
        
        # init instance of Manager
        man = Manager()
        
        # ip_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_=127001, port_=1883, topic_='foo', frequency_=1, channel_name_='bar')
        
        # port_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_='1883', topic_='foo', frequency_=1, channel_name_='bar')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=65536, topic_='foo', frequency_=1, channel_name_='bar')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=-1, topic_='foo', frequency_=1, channel_name_='bar')
            
        # topic_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_=42, frequency_=1, channel_name_='bar')

        # frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_='1', channel_name_='bar')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=0, channel_name_='bar')
            
        # channel_name_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_=42)

        # channel_limits_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', channel_limits_=42)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', channel_limits_=['-12.3', 13.5])
            
        # channel_frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', channel_frequency_='42')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', channel_frequency_=0)

        # novelty_frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', novelty_frequency_='42')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', novelty_frequency_=0)
            
        # novelty_duration_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', novelty_duration_='42')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', novelty_duration_=-42)
            
        # novelty_impact_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', novelty_impact_='42')

        # channel_name_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = man.create_pipeline(ip_='localhost', port_=1883, topic_='foo', frequency_=1, channel_name_='bar', pipeline_name_=42)