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
    await cl.setup()
    yield cl
    await cl._session.close()

@pytest.fixture
async def auth_client(credentials, loop):
    cl = ArangoClient(address=('localhost', 8529), loop=loop)
    await cl.setup()
    await cl.get_auth_token(*credentials)
    yield cl
    await cl._session.close()
