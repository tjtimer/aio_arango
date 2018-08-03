# aio_arango test_client
# created: 04.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com

from aio_arango.client import ArangoClient


def test_client_init(loop):
    client = ArangoClient()
    assert hasattr(client, 'user')
    assert hasattr(client, 'database')

async def test_client_login(client, credentials):
    resp = await client.login(*credentials)
    assert resp not in [None, '']
    assert 'errorMessage' not in resp.keys(), resp['errorMessage']
    print(*credentials, resp)
    assert client._auth_token == resp['jwt']

async def test_client_user_get(auth_client):
    response = await auth_client.user_get('testuwe')
    assert response.status < 300
    user = await response.json()
    print(user)
    assert isinstance(user, dict)

async def test_client_user_create(root_client, client):
    response = await root_client.user(json={'user': 'testuschi', 'passwd': 'testuschi'})
    assert response.status < 300
    user = await response.json()
    print(user)
    await test_client_login(client, ('testuschi', 'testuschi'))
    assert isinstance(user, dict)

async def test_client_user_delete(root_client, client):
    response = await root_client.user_delete('testuschi')
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    resp = await client.login('testuschi', 'testuschi')
    assert 'errorMessage' in resp.keys()
    assert 'Wrong credentials' in resp['errorMessage']
    print(data)
    assert isinstance(data, dict)
