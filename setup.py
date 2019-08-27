from setuptools import setup, find_packages
import unittest

setup(
    name='NoveltyProducer',
    version='0.0.2',
    description='python package to stream artificial data (including novelties) to a specific mqtt host.',
    packages=['NoveltyProducer'],
    test_suite='tests'
)