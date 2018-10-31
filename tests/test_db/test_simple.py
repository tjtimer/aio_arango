"""
test_simple
author: Tim "tjtimer" Jedro
created: 31.10.18
"""
from aio_arango.db import ArangoDB


async def test_collection_create_delete():
    name = 'collection1'
    async with ArangoDB('root', 'arango-pw', 'test-db') as db:
        clcs = await db.get_collections()
        assert name not in [c['name'] for c in clcs]
        await db.create_collection(name)
        clcs = await db.get_collections()
        assert name in [c['name'] for c in clcs]
        await db.collection1.add({'name': 'Jane'})
        await db.collection1.add({'name': 'John'})
        await db.collection1.add({'name': 'Jessi', 'age': 42})
        await db.collection1.add([{'name': 'Jerry', 'age': 66}, {'name': 'Jimi', 'age': 76}])
        entries = list(await db.collection1.all())
        assert len(entries) is 5
        await db.collection1.delete()
        clcs = await db.get_collections()
        assert name not in [c['name'] for c in clcs]

