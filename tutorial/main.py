from fastapi import FastAPI
from typing import Union
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

# Query Parameters with default values
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {skip : limit}

# Query Parameters with optional params
@app.get("/optional/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Query Parameters with type coneversion
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
# All urls are valid:
# http://127.0.0.1:8000/items/foo?short=1
# http://127.0.0.1:8000/items/foo?short=True
# http://127.0.0.1:8000/items/foo?short=true
# http://127.0.0.1:8000/items/foo?short=on
# http://127.0.0.1:8000/items/foo?short=yes

# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    return {user_id: item_id}

# Required query params
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name is ModelName.resnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    return {"model_name": model_name, "message": "Deep Learning FTW!"}

@app.get("/read/{file_path:path}")
async def read_file(file_path: str):
    return {"reading...   ": {file_path}}

@app.get("/items/{name}")
async def func1(name: int):
    return {"Message": name}

@app.get("/user/me")
async def func1():
    return {"Message": "current user details."}

@app.get("/user/{user_id}")
async def func1(user_id: int):
    return {"Message": f"{user_id} details."}

