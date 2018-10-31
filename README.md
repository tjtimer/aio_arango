# aio_arango
*Async Python driver for ArangoDB*

**[Read the docs here!](https://tjtimer.github.io/aio_arango/)**

## Getting Started

### Installation

```bash
pip install aio_arango
```  

### Usage

create a database:

```python
from aio_arango.client import ArangoAdmin

async def setup():
    async with ArangoAdmin('me', 'mypassword') as admin:
        await admin.create_db('mydb')
```

create a collection and add some documents:

```python
from aio_arango.db import ArangoDB

async def run():
    async with ArangoDB('me', 'mypassword', 'mydb') as db:
        await db.create_collection('collection1')
        await db.collection1.add({'name': 'Jane'})
        await db.collection1.add({'name': 'John'})
        await db.collection1.add({'name': 'Karl', 'age': 42})
        # or add a list of documents
        await db.collection1.add([{'name': 'Anna'}, {'name': 'Jacky', 'email': 'jacky@swag.com'}])
```
