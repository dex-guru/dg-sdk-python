from os.path import join, dirname

from setuptools import setup, find_packages

from dexguru_sdk import __version__

setup(
    name='dexguru-sdk',
    version=__version__,
    url='https://dex.guru',
    packages=find_packages(),
    license='MIT License',
    long_description_content_type='text/markdown',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=open('requirements.txt').read(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    test_suite='tests',
    project_urls={
        'Documentation': 'https://docs.dex.guru',
        'GitHub': 'https://github.com/dex-guru/dg-sdk-python',
        'Discord': 'https://discord.com/invite/dPW8fzwzz9',
    }
)
