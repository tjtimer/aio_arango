from pprint import pprint

from aio_arango.query import fetch_next


async def test_query(test_db):
    obj_counter = 0
    page_counter = 0
    async for page in test_db.query("FOR i IN 1..5000 RETURN {'idx': i, 'sqr': POW(i, 2)}"):
        page_counter += 1
        pprint(page)
        for obj in page['result']:
            obj_counter += 1
            assert 'idx' in obj.keys()
            assert 'sqr' in obj.keys()
            assert int(obj['idx'])**2 == int(obj['sqr'])
            print(f'page: {page_counter} obj {obj_counter} {obj["idx"]}: {obj["sqr"]}\n')
    assert obj_counter == 5000
    assert page_counter == 5000 / 25


async def test_query_cancelling(test_db):
    obj_counter = 0
    page_counter = 0
    query_id = None
    async for page in test_db.query("FOR i IN 1..5000 RETURN {'idx': i, 'sqr': POW(i, 2)}"):
        page_counter += 1
        query_id = page['id']
        for obj in page['result']:
            obj_counter += 1
            assert 'idx' in obj.keys()
            assert 'sqr' in obj.keys()
            assert int(obj['idx'])**2 == int(obj['sqr'])
            print(f'page: {page_counter} obj {obj_counter} {obj["idx"]}: {obj["sqr"]}\n')
        if page_counter >= 15:
            test_db._cancelled.append(query_id)
    assert obj_counter == 15 * 25
    assert page_counter == 15
    _id, response = await fetch_next(test_db, query_id)
    assert _id is None
