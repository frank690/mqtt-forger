# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().splitlines()

requirements = [req for req in requirements if not req.lower().startswith('pytest')]

setuptools.setup(
    name='mqtt-forger',
    version='0.1.16',
    author="frank690",
    author_email="admin@sffresch.de",
    description="Dynamic mqtt message broker with lots of fakery and witchcraft!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frank690/mqtt-forger",
    packages=setuptools.find_packages(exclude=['tests', 'tests.*', '*.tests.*', '*.tests', 'docs']),
    include_package_data=True,
    setup_requires=['cython'],
    install_requires=requirements,
    test_suite='tests',
    extras_require={
        "dev": [
            "pytest",
            "pytest_cov",
            "pytest-mock",
            "docstr-coverage==1.1.0",
            "pylint",
            "flake8",
            "freezegun",
        ],
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: Microsoft :: Windows ",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.7',
)