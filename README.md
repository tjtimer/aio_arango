# aio_arango
*Async Python driver for ArangoDB*

## Getting Started

### Installation

```bash
pip install aio_arango
```  

### Usage

create a database:

```python
from aio_arango.client import ArangoClient

async def setup():
    async with ArangoClient('me', 'mypassword') as cl:
        await cl.create_db('mydb')
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
```