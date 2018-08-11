async def foxx(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/foxx", **kwargs)


async def foxx_configuration(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/foxx/configuration", **kwargs)


async def foxx_configuration_update(client, **kwargs):
    return await client._session.request(
        "PATCH", f"{client.url_prefix}/_api/foxx/configuration", **kwargs)


async def foxx_configuration_replace(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/foxx/configuration", **kwargs)


async def foxx_dependencies(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/foxx/dependencies", **kwargs)


async def foxx_dependencies_update(client, **kwargs):
    return await client._session.request(
        "PATCH", f"{client.url_prefix}/_api/foxx/dependencies", **kwargs)


async def foxx_dependencies_replace(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/foxx/dependencies", **kwargs)


async def foxx_service(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/foxx/service", **kwargs)


async def foxx_service_install(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/foxx", **kwargs)


async def foxx_service_uninstall(client, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/foxx/service", **kwargs)


async def foxx_service_replace(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/foxx/service", **kwargs)


async def foxx_service_update(client, **kwargs):
    return await client._session.request(
        "PATCH", f"{client.url_prefix}/_api/foxx/service", **kwargs)


async def foxx_scripts(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/foxx/scripts", **kwargs)


async def foxx_scripts_post(client, name, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/foxx/scripts/{name}", **kwargs)


async def foxx_tests(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/foxx/tests", **kwargs)


async def foxx_development(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/foxx/development", **kwargs)


async def foxx_development_delete(client, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/foxx/development", **kwargs)


async def foxx_readme(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/foxx/readme", **kwargs)


async def foxx_swagger(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/foxx/swagger", **kwargs)


async def foxx_download(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/foxx/download", **kwargs)


async def foxx_commit(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/foxx/commit", **kwargs)
