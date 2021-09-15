from setuptools import setup, find_packages
from os.path import join, dirname
from src import __version__

setup(
    name='dex-guru-sdk',
    version=__version__,
    url='https://docs.dex.guru/',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'aiohttp==3.7.4.post0',
        'ujson==4.0.2',
        'pydantic==1.8.2',
    ],
    test_suite='tests'
)
