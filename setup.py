#name =!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='textify',
    version='0.0.1',
    description='Add songs to a Spotify playlist using Twilio',
    url='https://github.com/jingming/spotify/',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'spotify-python',
        'twilio'
    ]
)
