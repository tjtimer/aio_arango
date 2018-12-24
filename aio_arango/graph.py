from typing import Iterator

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
            data['orphanCollections'] = list(*self._orphan_collections)
        resp = await self._client.request("POST", f"{self.URL}", data)
        return await resp.json()

    async def delete(self, **kwargs):
        return await self._client.request(
            "DELETE", f"{self.url}", **kwargs)

    async def vertex(self, collection_name, vertex_key, **kwargs):
        return await self._client.request(
            "GET",
            f"{self.url}/vertex/{collection_name}/{vertex_key}",
            **kwargs)
    
    async def vertex_create(self, collection_name, **kwargs):
        return await self._client.request(
            "POST", f"{self.url}/vertex/{collection_name}",
            **kwargs)

    async def vertex_update(self, collection_name, vertex_key, **kwargs):
        return await self._client.request(
            "PATCH",
            f"{self.url}/vertex/{collection_name}/{vertex_key}",
            **kwargs)

    async def vertex_replace(self, collection_name, vertex_key, **kwargs):
        return await self._client.request(
            "PUT",
            f"{self.url}/vertex/{collection_name}/{vertex_key}",
            **kwargs)

    async def vertex_delete(self, collection_name, vertex_key, **kwargs):
        return await self._client.request(
            "DELETE",
            f"{self.url}/vertex/{collection_name}/{vertex_key}",
            **kwargs)

    async def edge(self, collection_name, edge_key, **kwargs):
        return await self._client.request(
            "GET",
            f"{self.url}/edge/{collection_name}/{edge_key}",
            **kwargs)

    async def edge_create(self, collection_name, **kwargs):
        return await self._client.request(
            "POST", f"{self.url}/edge/{collection_name}",
            **kwargs)

    async def edge_update(self, collection_name, edge_key, **kwargs):
        return await self._client.request(
            "PATCH",
            f"{self.url}/edge/{collection_name}/{edge_key}",
            **kwargs)

    async def edge_replace(self, collection_name, edge_key, **kwargs):
        return await self._client.request(
            "PUT",
            f"{self.url}/edge/{collection_name}/{edge_key}",
            **kwargs)

    async def edge_delete(self, collection_name, edge_key, **kwargs):
        return await self._client.request(
            "DELETE",
            f"{self.url}/edge/{collection_name}/{edge_key}",
            **kwargs)
