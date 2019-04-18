"""
test_graph.py
author: Tim "tjtimer" Jedro
created: 17.04.19
"""
from pprint import pprint

from aio_arango.db import DocumentType
from aio_arango.graph import ArangoGraph


async def test_graph_create(test_db):
    await test_db.create_collection('test_node')
    await test_db.create_collection('test_edge', doc_type=DocumentType.EDGE)
    await test_db.create_graph(
        'test_graph',
        [{'collection': 'test_edge', 'from': ['test_node'], 'to': ['test_node']}]
    )
    assert isinstance(test_db.test_graph, ArangoGraph)


async def test_graph_create_entries(test_graph):
    await test_graph.vertex_create('person', {'_key': 'jane', 'name': 'Jane', 'age': 23})
    await test_graph.vertex_create('person', {'_key': 'kalle', 'name': 'Kalle', 'age': 42})
    p_resp = await test_graph.vertex_create('person', {'_key': 'sven', 'name': 'Sven', 'age': 1})
    assert p_resp['_id'] == 'person/sven'
    b_resp = await test_graph.vertex_create('bike', {'_key': 'megacycle', 'brand': 'MegaCycle', 'weight': '2 kg'})
    assert b_resp['_id'] == 'bike/megacycle'
    await test_graph.vertex_create('bike', {'_key': 'diamant', 'brand': 'Diamant', 'weight': '12 kg'})
    await test_graph.edge_create('knows', {'_key': 'jane-kalle', '_from': 'person/jane', '_to': 'person/kalle'})
    await test_graph.edge_create('knows', {'_key': 'jane-sven', '_from': 'person/jane', '_to': 'person/sven'})
    await test_graph.edge_create('rides', {'_key': 'jane-megacycle', '_from': 'person/jane', '_to': 'bike/megacycle'})
    r_resp = await test_graph.edge_create('rides', {'_key': 'kalle-diamant', '_from': 'person/kalle', '_to': 'bike/diamant'})
    assert r_resp['_id'] == 'rides/kalle-diamant'

