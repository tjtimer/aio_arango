# aio_arango conftest
# created: 04.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com 
import pytest

from aio_arango.client import ArangoClient


@pytest.fixture
def credentials():
    return ('testuwe', 'testuwe')

@pytest.fixture
async def client(loop):
    cl = ArangoClient(address=('localhost', 8529), loop=loop)
    yield cl
    await cl.close()

@pytest.fixture
async def auth_client(credentials, loop):
    cl = ArangoClient(address=('localhost', 8529), loop=loop)
    await cl.login(*credentials)
    yield cl
    await cl.close()


@pytest.fixture
async def root_client(credentials, loop):
    cl = ArangoClient(address=('localhost', 8529), loop=loop)
    await cl.login('testroot', 'testpw')
    yield cl
    await cl.close()
