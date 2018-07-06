# aio_arango test_client
# created: 04.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com 

async def test_db_list_all(auth_client):
    resp = await auth_client.db_list_all()
    assert isinstance(resp, list)
    assert '_system' in resp


async def test_db_list_allowed(auth_client):
    resp = await auth_client.db_list_allowed()
    assert isinstance(resp, list)
    assert '_system' not in resp


async def test_db_current(auth_client):
    resp = await auth_client.db_current()
    assert isinstance(resp, dict)
    assert 'name' in resp
