from unittest import TestCase
from NoveltyProducer.engine.generator import Generator
from NoveltyProducer.engine.technician import Technican, InvalidInputTypeError, InvalidInputValueError
import datetime
import json

class TestBaseUnit(TestCase):

    def test_value_output(self):
        """Test output of each function."""
        
        # init instance of Generator
        generator_0 = Generator(name_='Foo', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_=1, dead_period_=0, seed_=42)
        generator_1 = Generator(name_='Bar', limits_=[-5, 5], frequency_=1, type_='random', dead_frequency_=1, dead_period_=0, seed_=42)
        generator_2 = Generator(name_='Bar', limits_=[-15, 15], frequency_=1, type_='fixed', dead_frequency_=1, dead_period_=1, seed_=42)
        # init instance of Technican
        techie = Technican({0:generator_0, 1:generator_1, 2:generator_2})
        
        # _get_unique_channels
        unique_channels = techie._get_unique_channels()
        self.assertEqual(unique_channels.sort(), ['Foo', 'Bar'].sort())
        
        # _get_overall_output
        bt_0 = generator_0.basetime
        bt_01 = bt_0 + datetime.timedelta(seconds=0.25)
        self.assertTrue(techie._get_overall_output('Foo', time_=bt_01) == 15)
        self.assertTrue(techie._get_overall_output('Foo') <= 15)
        self.assertTrue(techie._get_overall_output('Foo') >= -15)
        self.assertTrue(techie._get_overall_output('Bar') <= 5)
        self.assertTrue(techie._get_overall_output('Bar') >= -5)
        
        # get_payload
        jdata = techie.get_payload()
        data = json.loads(jdata)
        self.assertTrue("timestamp" in data.keys())
        self.assertTrue("Foo" in data.keys())
        self.assertTrue("Bar" in data.keys())
        
    def test_type_output(self):
        """Test types of output"""
        
        # init instance of Generator
        generator = Generator(name_='Foo', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_=1, dead_period_=0, seed_=42)
        # init instance of Technican
        techie = Technican({0:generator})
        
        # _get_unique_channels
        unique_channels = techie._get_unique_channels()
        self.assertIsInstance(unique_channels, list)

        # _get_overall_output
        self.assertIsInstance(techie._get_overall_output('Foo'), float)

        # get_payload
        jdata = techie.get_payload()
        self.assertIsInstance(jdata, str)
        data = json.loads(jdata)
        self.assertIsInstance(data, dict)

    def test_invalid_inputs(self):
        """Test for all expected errors that should be raised when given invalid inputs"""
       
        # generators_
        with self.assertRaises(InvalidInputTypeError):
            Technican(42)
        with self.assertRaises(InvalidInputValueError):
            Technican({'some':'dictionary'})