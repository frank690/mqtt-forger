import numpy as np
from unittest import TestCase
from NoveltyProducer.engine.generator import Generator, InvalidInputTypeError, InvalidInputValueError, SeedReplantError
import datetime

class TestBaseUnit(TestCase):

    def test_type_output(self):
        """Test types of output"""
        
        # init class
        generator = Generator(name_='Foo', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_=1, dead_period_=0, seed_=42)
    
        # _seconds_since_init
        seconds = generator._seconds_since_init()
        self.assertIsInstance(seconds, float)

        # _rescale
        rescale_data_type = type(generator._rescale(0.5))
        self.assertTrue(issubclass(rescale_data_type, (float, np.floating)))

        # get_data
        data_type = type(generator.get_data(datetime.datetime.now()))
        self.assertTrue(issubclass(data_type, (float, np.floating)))

        
    def test_value_output(self):
        """Test delivered output of each function of generator class."""
        
        # init class
        generator = Generator(name_='Foo', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_=1, dead_period_=0, seed_=42)
        
        # replant the seed
        generator._plant_a_seed()
        
        # _seconds_since_init
        seconds = generator._seconds_since_init(generator.basetime)
        self.assertTrue(seconds == 0)
        seconds = generator._seconds_since_init()
        self.assertTrue(seconds > 0)
        
        # _rescale
        min_rescaled = generator._rescale(-1)
        self.assertTrue(min_rescaled == -15)
        max_rescaled = generator._rescale(1)
        self.assertTrue(max_rescaled == 15)
        
        # get_data
        self.assertTrue(generator.get_data(generator.basetime) == 0)
        self.assertTrue(generator.get_data(generator.basetime + datetime.timedelta(seconds=0.25)) >= 14.99999999)
        self.assertTrue(generator.get_data(generator.basetime + datetime.timedelta(seconds=0.5)) <= 0.0000001)
        self.assertTrue(generator.get_data(generator.basetime + datetime.timedelta(seconds=0.5)) >= -0.0000001)
        self.assertTrue(generator.get_data(generator.basetime + datetime.timedelta(seconds=0.75)) <= -14.99999999)
        
        # init another class
        generator = Generator(name_='Foo', limits_=[-15, 15], frequency_=1, type_='fixed', dead_frequency_=1, dead_period_=0, seed_=42)
        generator._plant_a_seed(123)
        self.assertTrue(generator.get_data(generator.basetime) >= 14.99999999)

    def test_invalid_inputs(self):
        """Test for all expected errors that should be raised when given invalid inputs"""
        # channel_name_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator(name_=1337, limits_=[-15, 15], frequency_=1, dead_frequency_=0.1, dead_period_=2)

        # channel_limits_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator(name_='ThisWillFail', limits_='InvalidLimits', frequency_=1, type_='sin', dead_frequency_=0.1, dead_period_=2)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=['InvalidLimit', 15], frequency_=1, type_='sin', dead_frequency_=0.1, dead_period_=2)
            
        # channel_frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_='InvalidChannelFrequency', type_='sin', dead_frequency_=0.1, dead_period_=2)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_=0, type_='sin', dead_frequency_=0.1, dead_period_=2)
            
        # type_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_=1, type_=1, dead_frequency_=0.1, dead_period_=2)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_=1, type_='fail', dead_frequency_=0.1, dead_period_=2)
            
        # dead_frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_='InvalidDeadFrequency', dead_period_=2)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_=0, dead_period_=2)
            
        # dead_period_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_=0.1, dead_period_='InvalidDeadPeriod')
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_=0.1, dead_period_=-2)
            
        # seed_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_=0.1, dead_period_=2, seed_='InvalidSeed')
        with self.assertRaises(SeedReplantError):
            invalid_generator = Generator(name_='ThisWillFail', limits_=[-15, 15], frequency_=1, type_='sin', dead_frequency_=0.1, dead_period_=2)
            invalid_generator._plant_a_seed()