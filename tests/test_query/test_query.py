from aio_arango.db import ArangoDB


async def test_query():
    async with ArangoDB('root', 'arango-pw', '_system') as db:
        counter = 0
        async for obj in db.query("FOR i IN 1..5000 RETURN {'idx': i, 'sqr': POW(i, 2)}"):
            counter += 1
            assert 'idx' in obj.keys()
            assert 'sqr' in obj.keys()
            assert int(obj['idx'])**2 == int(obj['sqr'])
            print(f'obj {counter} {obj["idx"]}: {obj["sqr"]}\n')
        assert counter == 5000
