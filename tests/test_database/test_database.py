from pprint import pprint

from aio_arango import database as db


async def test_create(root_client):
    response = await db.create(root_client, name='test1-db')
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    pprint(data)


async def test_delete(root_client):
    response = await db.delete(root_client, name='test1-db')
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    pprint(data)


async def test_create_with_users(root_client, users):
    response = await db.create(root_client,
                               name='test1-db',
                               users=users)
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    pprint(data)
    await db.delete(root_client, name='test1-db')


async def test_current(root_client):
    response = await db.current(root_client)
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    pprint(data)


async def test_list_for_root(root_client):
    response = await db.list(root_client)
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    pprint(data)


async def test_list_for_user(user_client):
    user_client.db_name = 'test-db'
    response = await db.list(user_client)
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    pprint(data)

