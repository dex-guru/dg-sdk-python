from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='DexGuru SDK',
    version='0.0.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=[
        'aiohttp==3.7.4.post0',
        'ujson==4.0.2',
        'pydantic==1.8.2',
    ],
    test_suite='tests'
)
