"""
test_create_db
author: Tim "tjtimer" Jedro
created: 31.10.18
"""
from aio_arango.client import ArangoAdmin


async def test_create_and_delete_db_valid():
    name = 'test-tmp-db'
    async with ArangoAdmin('root', 'arango-pw') as admin:
        assert name not in admin._databases
        await admin.create_db(name)
        assert name in admin._databases
        await admin.delete_db(name)
        assert name not in admin._databases
