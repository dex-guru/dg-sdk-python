from os.path import join, dirname

from setuptools import setup, find_packages

from src import __version__

setup(
    name='dex-guru-sdk',
    version=__version__,
    url='https://docs.dex.guru/',
    packages=find_packages(),
    license='MIT License',
    long_description_content_type='text/markdown',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'aiohttp==3.7.4.post0',
        'ujson==4.0.2',
        'pydantic==1.8.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    test_suite='tests',
    project_urls={
        'GitHub': 'https://github.com/dex-guru/dg-sdk-python'}
)
