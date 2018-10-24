"""
admin
author: Tim "tjtimer" Jedro
created: 19.10.18
"""
from typing import Optional

from aio_arango.client import ArangoClient


class ArangoAdmin(ArangoClient):

    async def create_db(self, name: str, users: list=None):
        if users is None:
            return await self.request('POST', f'/_api/database', {'name': name})
        return await self.request(
            'POST', f'/_api/database',
            {'name': name, 'users': users}
        )

    async def delete_db(self, name: str):
        return await self.request('DELETE', f'/_api/database/{name}')

    async def create_user(self,
                          name: str, password: str,
                          active: Optional[bool]=None,
                          extra: Optional[dict]=None):
        user_data = dict(user=name, passwd=password)
        if active is None:
            active = True
        user_data['active'] = active
        if isinstance(extra, dict):
            user_data['extra'] = extra
        return await self.request(
            'POST', f'/_api/user', data=user_data)

