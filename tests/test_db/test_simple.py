"""
test_simple
author: Tim "tjtimer" Jedro
created: 31.10.18
"""
from pprint import pprint


async def test_collection_create_read_update_delete(loop, test_db):
    db, name = test_db, 'collection1'
    collections = await db.get_collections()
    assert name not in [c['name'] for c in collections]
    await db.create_collection(name)
    collections = await db.get_collections()
    assert name in [c['name'] for c in collections]
    await db.collection1.add({'name': 'Jane'})
    await db.collection1.add({'name': 'John'})
    await db['collection1'].add({'_key': 'rumbumski', 'name': 'Jessi', 'age': 42})
    await db.collection1.add([{'name': 'Jerry', 'age': 66}, {'name': 'Jimi', 'age': 76}])
    entries = list(await db.collection1.all())
    assert len(entries) is 5
    pprint(entries)
    await db.collection1.delete()
    collections = await db.get_collections()
    assert name not in [c['name'] for c in collections]
