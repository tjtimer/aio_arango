import asyncio
from pprint import pprint

from aio_arango import database as db


async def test_create(db_client):
    response = await db.collection_create(db_client, json={'name': 'testCollection'})
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    pprint(data)


async def test_delete(db_client):
    response = await db.collection_delete(db_client, name='testCollection')
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    pprint(data)


async def test_create_with_props(db_client):
    json = {
        'name': 'testCollectionWP',
        'keyOptions': {
            'allowUserKeys': False,
            'type': 'autoincrement',
            'increment': 2
        }
    }
    response = await db.collection_create(db_client, json=json)
    assert response.status < 300
    data = await response.json()
    assert data['error'] is False
    pprint(data)
    await db.collection_delete(db_client, name='testCollectionWP')


async def test_create_concurrent(db_client):
    clt_list =[{
        'name': f'testCollection-{idx}',
        'keyOptions': {
            'allowUserKeys': bool(idx % 3 > 0),
            'type': 'autoincrement',
            'increment': int((idx % 3) + 1)
        }
    } for idx in range(50)]
    done, _ = await asyncio.wait(
        [db.collection_create(db_client, json=data) for data in clt_list]
    )
    for task in done:
        response = task.result()
        print(response)
        data = await response.json()
        assert data['error'] is False
        pprint(data)


async def test_delete_concurrent(db_client):
    clt_list = [f'testCollection-{idx}' for idx in range(50)]
    done, _ = await asyncio.wait(
        [db.collection_delete(db_client, name=name) for name in clt_list]
    )
    print('deleted')
    for task in done:
        response = task.result()
        print(response)
        data = await response.json()
        assert data['error'] is False
        pprint(data)

