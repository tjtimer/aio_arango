# aio_arango test_client
# created: 04.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
from aio_arango.client import ArangoClient


def test_client_init():
    client = ArangoClient()
    assert hasattr(client, 'user')
    print(client.user.help)
    assert hasattr(client, 'database')


async def test_client_login(client, credentials):
    token = await client.login(*credentials)
    assert token not in [None, '']
    assert client._auth_token == token

async def test_client_user_get(auth_client):
    response = await auth_client.user_get(url_vars={'user': 'testuwe'})
    assert response.status < 300
    user = await response.json()
    print(user)
    assert isinstance(user, dict)


async def test_client_user_create(root_client):
    response = await root_client.user(json={'user': 'testuschi', 'password': 'testuschi'})
    print(root_client.user.help)
    assert response.status < 300
    user = await response.json()
    print(user)
    assert isinstance(user, dict)


async def test_client_user_delete(root_client):
    response = await root_client.user_delete(url_vars={'user': 'testuschi'})
    print(root_client.user_delete.help)
    assert response.status < 300
    data = await response.json()
    print(data)
    assert isinstance(data, dict)
