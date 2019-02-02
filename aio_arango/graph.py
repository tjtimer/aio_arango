from typing import Iterator, Optional

from aio_arango.client import ArangoClient


class ArangoGraph:
    URL = '/_api/gharial'

    def __init__(self,
                 client: ArangoClient,
                 name: str,
                 edges: list,
                 orphans: list = None):
        self._name = name
        self._edge_definitions = edges
        self._orphan_collections = orphans
        self._client = client

    @property
    def url(self):
        return f'{self.URL}/{self._name}'

    async def get(self):
        return await self._client.request("GET", f"{self.url}")

    @classmethod
    async def all(cls, client: ArangoClient):
        resp = await client.request("GET", f"{cls.URL}")
        return (await resp.json())['graphs']

    async def create(self):
        data = {'name': self._name, 'edgeDefinitions': self._edge_definitions}
        if isinstance(self._orphan_collections, Iterator):
            data['orphanCollections'] = [*self._orphan_collections]
        resp = await self._client.request("POST", f"{self.URL}", data)
        return await resp.json()

    async def add_edge_definition(self, definition: dict):
        resp = await self._client.request("POST", f"{self.url}/edge", definition)
        return await resp.json()

    async def delete(self):
        return await self._client.request("DELETE", f"{self.url}")

    async def vertex(self, _id):
        return await self._client.request(
            "GET",
            f"{self.url}/vertex/{_id}")

    async def vertex_create(self, collection_name, data, **kwargs):
        resp = await self._client.request(
            "POST",
            f"{self.url}/vertex/{collection_name}",
            data, **kwargs)
        return (await resp.json())['vertex']

    async def vertex_update(self, _id, data, **kwargs):
        resp = await self._client.request(
            "PATCH",
            f"{self.url}/vertex/{_id}",
            data, **kwargs)
        return (await resp.json())['vertex']

    async def vertex_replace(self, _id, data):
        return await self._client.request(
            "PUT",
            f"{self.url}/vertex/{_id}",
            data)

    async def vertex_delete(self, _id, data):
        return await self._client.request(
            "DELETE",
            f"{self.url}/vertex/{_id}",
            data)

    async def edge(self, _id, **kwargs):
        return await self._client.request(
            "GET",
            f"{self.url}/edge/{_id}",
            **kwargs)

    async def edge_create(self, collection_name, data, **kwargs):
        resp = await self._client.request(
            "POST", f"{self.url}/edge/{collection_name}", data, **kwargs)
        return (await resp.json())['edge']

    async def edge_update(self, _id, **kwargs):
        resp = await self._client.request(
            "PATCH",
            f"{self.url}/edge/{_id}",
            **kwargs)
        return (await resp.json())['edge']

    async def edge_replace(self, _id, **kwargs):
        return await self._client.request(
            "PUT",
            f"{self.url}/edge/{_id}",
            **kwargs)

    async def edge_delete(self, _id, **kwargs):
        return await self._client.request(
            "DELETE",
            f"{self.url}/edge/{_id}",
            **kwargs)


class ArangoGraphQuery:

    def __init__(self,
                 graph_name: str, *,
                 depth: Optional['int, float, list, tuple'] = None,
                 direction: str = None,
                 returning: str = None):
        if direction is None:
            direction = 'ANY'
        if returning is None:
            returning = 'v'

        self._depth = depth
        self._direction = direction.upper()
        self._returning = returning
        self._graph_name = graph_name
        self._modifiers = []

        self.start_vertex = None

    @property
    def depth(self):
        depth = self._depth
        if depth is None:
            depth = (1, 1)
        elif isinstance(depth, (int, float)):
            depth = (abs(int(depth)), abs(int(depth)))
        start, stop = sorted(depth)[:2]
        return f'{start}..{stop}'

    @depth.setter
    def depth(self, value):
        self._depth = value

    @property
    def statement(self):
        return (f'FOR v, e, p IN {self._direction} \"{self.start_vertex}\" '
                f'GRAPH \"{self._graph_name}\" '
                f'{" ".join(self._modifiers)} RETURN {self._returning}')

    def lt(self, left, right):
        self._modifiers.append(f'FILTER {left} < {right}')
        return self

    def lte(self, left, right):
        self._modifiers.append(f'FILTER {left} <= {right}')
        return self

    def eq(self, left, right):
        self._modifiers.append(f'FILTER {left} == {right}')
        return self

    def neq(self, left, right):
        self._modifiers.append(f'FILTER {left} != {right}')
        return self

    def like(self, left, right):
        self._modifiers.append(f'FILTER {left} LIKE {right}')
        return self

    def limit(self, size: int, offset: int = None):
        if offset is None:
            offset = 0
        self._modifiers.append(f'LIMIT {abs(int(offset))}, {abs(int(size))}')
        return self

    def asc(self, field):
        self._modifiers.append(f'SORT {field} ASC')

    def desc(self, field):
        self._modifiers.append(f'SORT {field} DESC')

    async def exec(self, client):
        async for obj in client.query(self.statement):
            yield obj
