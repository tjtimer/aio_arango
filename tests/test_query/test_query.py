from aio_arango.db import ArangoDB


async def test_query():
    async with ArangoDB('root', 'arango-pw', '_system') as db:
        counter = 0
        async for obj in db.query("FOR i IN 1..5000 RETURN {'idx': i, 'sqr': i POW 2}"):
            assert 'idx' in obj.keys()
            assert 'sqr' in obj.keys()
            assert int(obj['idx'])**2 == int(obj['sqr'])
            counter += 1
        assert counter == 5000
