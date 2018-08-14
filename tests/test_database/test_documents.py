from pprint import pprint

from aio_arango import database as db


async def test_create(db_client):
    await db.collection_create(db_client, json={'name': 'testCollection'})
    response = await db.document_create(
        db_client,
        collection='testCollection',
        json={'_key': 'testDoc-Single', 'ToDo': 'finish something'})
    assert response.status < 300
    data = await response.json()
    pprint(data)


async def test_delete(db_client):
    response = await db.document_delete(
        db_client, handle='testCollection/testDoc-Single'
    )
    assert response.status < 300
    data = await response.json()
    pprint(data)
    await db.collection_delete(db_client, name='testCollection')
