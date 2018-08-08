# aio_arango conftest
# created: 04.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com 
import pytest

from aio_arango.client import ArangoClient


# pytest_plugins = 'aiohttp.pytest_plugin'

@pytest.fixture
def credentials():
    return ('testuwe', 'testuwe')

@pytest.fixture(scope="function")
async def client(loop):
    cl = ArangoClient(address=('localhost', 8529), loop=loop)
    yield cl
    await cl.close()

@pytest.fixture(scope="function")
async def user_client(credentials, loop):
    cl = ArangoClient(address=('localhost', 8529), loop=loop)
    await cl.login(*credentials)
    yield cl
    await cl.close()


@pytest.fixture(scope="function")
async def root_client(loop):
    cl = ArangoClient(address=('localhost', 8529), loop=loop)
    await cl.login('testroot', 'testpw')
    yield cl
    await cl.close()
