# aio_arango setup
# created: 01.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com 
from setuptools import find_packages, setup

setup(
        name='aio_arango',
        short_description='Async Python ArangoDB adapter.',
        author='Tim "tjtimer" Jedro',
        author_email='tjtimer@gmail.com',
        packages=find_packages('aio_arango'),
        install_requires=('aiohttp', 'PyYaml', 'pytest', 'pytest-aiohttp')
)
