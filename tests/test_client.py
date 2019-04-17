"""
test_client
author: Tim "tjtimer" Jedro
created: 24.10.18
"""

from aiohttp import ClientSession

from aio_arango.client import ArangoClient


async def test_client_login():
    cl = ArangoClient('root', 'arango-pw')
    assert cl.is_authenticated is False
    await cl.login()
    assert cl.is_authenticated is True
    assert cl._headers.get('Authorization') is not None
    assert isinstance(cl._session, ClientSession)
    assert cl._ArangoClient__credentials is None


async def test_client_close():
    cl = ArangoClient('root', 'arango-pw')
    await cl.login()
    assert cl.is_authenticated is True
    assert cl._headers.get('Authorization') is not None
    await cl.close()
    assert cl._session is None
    assert cl.is_authenticated is False
    assert 'Authorization' not in cl._headers.keys()


async def test_client_context_manager():
    async with ArangoClient('root', 'arango-pw') as cl:
        assert cl.is_authenticated is True
        assert cl._headers.get('Authorization') is not None
    assert cl._session is None
    assert cl.is_authenticated is False
    assert 'Authorization' not in cl._headers.keys()
