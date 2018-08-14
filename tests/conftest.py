# aio_arango conftest
# created: 04.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import math

import pytest

from aio_arango.client import ArangoClient


@pytest.fixture
def credentials():
    return ('testuwe', 'testuwe')


@pytest.fixture
def users():
    return [{'name': 'testuwe', 'passwd': 'testuwe', 'active': True},
            {'name': 'JaneDoe', 'passwd': 'janeDoe', 'active': True},
            {'name': 'Some1', 'passwd': 'someone', 'active': True}]

@pytest.fixture
def collections():
    return [{
        'name': f'testCollection-{idx}',
        'keyOptions': {
            'allowUserKeys': bool(idx % 3 > 0),
            'type': 'autoincrement',
            'increment': int((idx % 3) + 1)
        }
    } for idx in range(50)]


@pytest.fixture
def documents():
    return [{
        'name': f'testDocument-{idx}',
        'otherStr': f'{idx % 4} - {idx**(idx%4)}',
        'anInt': idx,
        'aFloat': float(idx) / (idx * math.pi)
    } for idx in range(50)]


@pytest.fixture
def db_name():
    return 'test-db'

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


@pytest.fixture(scope="function")
async def db_client(root_client, user_client, db_name, loop):
    cl = ArangoClient(address=('localhost', 8529), loop=loop)
    await cl.login(*credentials)
    cl.db_name = db_name
    yield cl
    await cl.close()
