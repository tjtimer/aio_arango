from typing import Iterator


async def graph(client, graph_name, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/gharial/{graph_name}", **kwargs)


async def create(client, *,
                 name: str = None, edge_def: dict = None,
                 orphan_collections: Iterator = None):
    json = {'name': name, 'edgeDefinition': edge_def}
    if isinstance(orphan_collections, Iterator):
        json['orphanCollections'] = list(*orphan_collections)
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/gharial", json=json)


async def delete(client, graph_name, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/gharial/{graph_name}", **kwargs)


async def vertex(client, graph_name, collection_name, vertex_key, **kwargs):
    return await client._session.request(
        "GET",
        f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
        **kwargs)


async def vertex_create(client, graph_name, collection_name, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}",
        **kwargs)


async def vertex_update(client, graph_name, collection_name, vertex_key, **kwargs):
    return await client._session.request(
        "PATCH",
        f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
        **kwargs)


async def vertex_replace(client, graph_name, collection_name, vertex_key, **kwargs):
    return await client._session.request(
        "PUT",
        f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
        **kwargs)


async def vertex_delete(client, graph_name, collection_name, vertex_key, **kwargs):
    return await client._session.request(
        "DELETE",
        f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
        **kwargs)


async def edge(client, graph_name, collection_name, edge_key, **kwargs):
    return await client._session.request(
        "GET",
        f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
        **kwargs)


async def edge_create(client, graph_name, collection_name, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}",
        **kwargs)


async def edge_update(client, graph_name, collection_name, edge_key, **kwargs):
    return await client._session.request(
        "PATCH",
        f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
        **kwargs)


async def edge_replace(client, graph_name, collection_name, edge_key, **kwargs):
    return await client._session.request(
        "PUT",
        f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
        **kwargs)


async def edge_delete(client, graph_name, collection_name, edge_key, **kwargs):
    return await client._session.request(
        "DELETE",
        f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
        **kwargs)
