from aio_arango.db import ArangoDB
from aio_arango.query import query


async def test_query():
    async with ArangoDB('root', 'arango-pw', '_system') as db:
        counter = 0
        async for obj in query(db, "FOR i IN 1..5000 RETURN {'idx': i, 'sqr': POW(i, 2)}", size=5):
            assert 'idx' in obj.keys()
            assert 'sqr' in obj.keys()
            assert int(obj['idx'])**2 == int(obj['sqr'])
            print(f'obj {obj["idx"]}: {obj["sqr"]}\n')
            counter += 1
        assert counter == 5000
