import numpy as np
from unittest import TestCase
from NoveltyProducer.Generator import Generator, InvalidInputTypeError, InvalidInputValueError, SeedReplantError

class TestBaseUnit(TestCase):

    def test_type_output(self):
        """Test types of output"""
        
        # init class
        seed = 42
        generator = Generator('Test', [-15, 15], 1, 1, 1, 3, seed)
    
        # _get_clean_data
        clean_data = generator._get_clean_data()
        clean_data_type = type(clean_data)
        self.assertTrue(issubclass(clean_data_type, (float, np.floating)))

        # _get_noise
        noise_data_type = type(generator._get_clean_data())
        self.assertTrue(issubclass(noise_data_type, (float, np.floating)))

        # _get_times
        self.assertTrue(isinstance(generator._get_times(), tuple))  

        # _rescale
        rescale_data_type = type(generator._rescale(clean_data))
        self.assertTrue(issubclass(rescale_data_type, (float, np.floating)))

        # get_data
        data_type = type(generator.get_data())
        self.assertTrue(issubclass(data_type, (float, np.floating)))
        
        # get_payload
        self.assertTrue(isinstance(generator.get_payload(), str))
        
    def test_value_output(self):
        """Test delivered output of each function of generator class."""
        
        # init class
        seed = 42
        generator = Generator('Test', [-15, 15], 1, 1, 1, 3, seed)
        
        # replant the seed
        generator._plant_a_seed()
        
        # _get_times
        times = generator._get_times()
        
        # _get_clean_data
        clean_data_value = generator._get_clean_data(times)
        self.assertTrue(clean_data_value <= max(generator.channel_limits))
        self.assertTrue(clean_data_value >= min(generator.channel_limits))
        
        # _get_noise
        noise_data_value = generator._get_noise(times)
        self.assertTrue(noise_data_value <= generator.novelty_impact)
        self.assertTrue(noise_data_value >= -generator.novelty_impact)
        self.assertTrue(generator._get_noise() <= generator.novelty_impact)
        self.assertTrue(generator._get_noise() >= -generator.novelty_impact)
        
        # replant the seed
        generator._plant_a_seed()
        
        # get_data
        data_value = generator.get_data(times)
        self.assertTrue(data_value == clean_data_value + noise_data_value)
        
        # _plant_a_seed
        generator._plant_a_seed(123)
        
    def test_invalid_inputs(self):
        """Test for all expected errors that should be raised when given invalid inputs"""
        # channel_name_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator(1337, [-15, 15], 1, 0.1, 2, 3)
        
        # channel_limits_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator('ThisWillFail', 'InvalidLimits', 1, 0.1, 2, 3)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = Generator('ThisWillFail', ['InvalidLimit', 15], 1, 0.1, 2, 3)
            
        # channel_frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator('ThisWillFail', [-15, 15], 'InvalidChannelFrequency', 0.1, 2, 3)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = Generator('ThisWillFail', [-15, 15], 0, 0.1, 2, 3)
            
        # novelty_frequency_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator('ThisWillFail', [-15, 15], 1, 'InvalidNoveltyFrequency', 2, 3)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = Generator('ThisWillFail', [-15, 15], 1, 0, 2, 3)
            
        # novelty_duration_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator('ThisWillFail', [-15, 15], 1, 0.1, 'InvalidNoveltyDuration', 3)
        with self.assertRaises(InvalidInputValueError):
            invalid_generator = Generator('ThisWillFail', [-15, 15], 1, 0.1, -2, 3)
            
        # novelty_impact_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator('ThisWillFail', [-15, 15], 1, 0.1, 2, 'InvalidNoveltyImpact')
            
        # seed_
        with self.assertRaises(InvalidInputTypeError):
            invalid_generator = Generator('ThisWillFail', [-15, 15], 1, 0.1, 2, 3, 'InvalidSeed')
        with self.assertRaises(SeedReplantError):
            invalid_generator = Generator('ThisWillFail', [-15, 15], 1, 0.1, 2, 3)
            invalid_generator._plant_a_seed()