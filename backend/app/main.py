from typing import Union
from fastapi import FastAPI
from aiohttp import ClientSession

app = FastAPI()
session = ClientSession()
nlu_server = 'http://192.168.0.14:5005/model/parse'

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/nlu/{text}")
async def read_root(text: str):
    async with session.post(nlu_server, json={'text': text}) as response:
        result = await response.json()
    return result

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
