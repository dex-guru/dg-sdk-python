from setuptools import setup, find_packages
from os.path import join, dirname
from src import version

setup(
    name='DexGuru SDK',
    version=version,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'aiohttp==3.7.4.post0',
        'ujson==4.0.2',
        'pydantic==1.8.2',
    ],
    test_suite='tests'
)
