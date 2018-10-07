# aio_arango test_client
# created: 04.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
from pprint import pprint

from aio_arango.client import ArangoClient


def test_client_init(loop):
    client = ArangoClient()
    assert hasattr(client, 'user')
    assert hasattr(client, 'database')

async def test_client_login(client, credentials):
    resp = await client.login(*credentials)
    assert resp not in [None, '']
    assert 'errorMessage' not in resp.keys(), resp['errorMessage']
    assert client._auth_token == resp['jwt']

async def test_client_user_get(user_client):
    response = await user_client.user_get('testuwe')
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


async def test_client_collection_get_no_params(root_client):
    response = await root_client.collection()
    assert response.status < 300
    collections = await response.json()
    print('collections without params')
    pprint(collections)
    assert isinstance(collections, dict)


async def test_client_collection_get_with_params(root_client):
    response = await root_client.collection(exclude_system=0)
    assert response.status < 300
    collections = (await response.json())['result']
    print('collections with params')
    pprint(collections)
    assert isinstance(collections, list)


async def test_client_collection_load_no_kwargs(db_client):
    response = await db_client.collection_load('account')
    assert response.status < 300
    data = await response.json()
    print('collection_load')
    pprint(data)
    assert data['name'] == 'account'
    assert data['isSystem'] is False
    assert 'count' in data.keys()


async def test_client_collection_unload(db_client):
    response = await db_client.collection_unload('account')
    assert response.status < 300
    data = await response.json()
    print('collection_unload')
    pprint(data)
    assert data['name'] == 'account'

async def test_client_collection_load_with_kwargs(db_client):
    response = await db_client.collection_load(
        'worksAt',
        count=False
    )
    pprint(response.request_info)
    assert response.status < 300
    data = await response.json()
    print('collection_load count: False')
    pprint(data)
    assert data['name'] == 'worksAt'
    assert data['isSystem'] is False
    assert 'count' not in data.keys()
    await db_client.collection_unload('worksAt')
