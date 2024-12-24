# FastAPI

- [FastAPI](#fastapi)
  - [Path Parameters](#path-parameters)
    - [Path parameters with types](#path-parameters-with-types)
    - [Data validation](#data-validation)
    - [Order matters](#order-matters)
    - [Predefined values](#predefined-values)
      - [Create Enum class](#create-enum-class)
      - [Declare a path parameter](#declare-a-path-parameter)
      - [Compare enumeration members](#compare-enumeration-members)
      - [Get enumeration value](#get-enumeration-value)
    - [Path parameters containing paths](#path-parameters-containing-paths)
      - [Path convertor](#path-convertor)
  - [Query Parameters](#query-parameters)
    - [Defaults query parameters](#defaults-query-parameters)
    - [Optional query parameters](#optional-query-parameters)
    - [Query parameter type conversion](#query-parameter-type-conversion)
    - [Multiple path and query parameters](#multiple-path-and-query-parameters)
    - [Required query parameters](#required-query-parameters)


The simplest FastAPI file could look like this
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

**Create a path operation**

"Path" here refers to the last part of the URL starting from the first `/`.

So, in a URL like:
```console
https://example.com/items/foo
```
...the path would be:
```console
/items/foo
```

**Operation**

"Operation" here refers to one of the HTTP "methods".

One of:
* `POST` : to create data.
* `GET` : to read data.
* `PUT` : to update data.
* `DELETE` : to delete data.
  
...and the more exotic ones:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

**Path operation decorator**

```python
@app.get("/")
```
The `@app.get("/")` tells FastAPI that the function right below is in charge of handling requests that go to:
* the path `/`
* using a `get` operation

**Path operation function**

* path: is `/`.
* operation: is `get`.
* function: is the function below the "decorator" (below `@app.get("/")`).

**Recap**

* Import FastAPI.
* Create an app instance.
* Write a path operation decorator using decorators like `@app.get("/")`.
* Define a path operation function; for example, `def root(): ....`

<br>

## Path Parameters
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```
The value of the path parameter `item_id` will be passed to your function as the argument `item_id`.

So, if you run this example and go to `http://127.0.0.1:8000/items/foo`, you will see a response of:

```json
{"item_id":"foo"}
```

### Path parameters with types
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

In this case, item_id is declared to be an int.

If you run this example and open your browser at `http://127.0.0.1:8000/items/3`, you will see a response of:

```console
{"item_id":3}
```

### Data validation
But if you go to the browser at `http://127.0.0.1:8000/items/foo`, you will see a nice HTTP error of:

```console
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo",
      "url": "https://errors.pydantic.dev/2.1/v/int_parsing"
    }
  ]
}
```
> because the path parameter item_id had a value of "foo", which is not an int.


### Order matters
When creating path operations, you can find situations where you have a fixed path.

Like `/users/me`, let's say that it's to get data about the current user.

And then you can also have a path `/users/{user_id}` to get data about a specific user by some user ID.

Because path operations are evaluated in order, you need to make sure that the path for `/users/me` is declared before the one for `/users/{user_id}`:

```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

Otherwise, the path for `/users/{user_id}` would match also for `/users/me`, "thinking" that it's receiving a parameter `user_id` with a value of "me".

### Predefined values
If you have a path operation that receives a path parameter, but you want the possible valid path parameter values to be predefined, you can use a standard Python `Enum`.

#### Create Enum class
```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
```
#### Declare a path parameter
Then create a path parameter with a type annotation using the enum class you created (ModelName):
```python
async def get_model(model_name: ModelName):
```

#### Compare enumeration members
```python
    if model_name is ModelName.alexnet:
```

#### Get enumeration value
```python
    if model_name.value == "lenet":
```

Full code:
```python
from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

### Path parameters containing paths
Let's say you have a path operation with a path `/files/{file_path}`.

But you need file_path itself to contain a path, like `home/johndoe/myfile.txt`.

So, the URL for that file would be something like: `/files/home/johndoe/myfile.txt`.

`OpenAPI doesn't support` a way to declare a path parameter to contain a path inside

#### Path convertor
Using an option directly from `Starlette` you can declare a path parameter containing a path using a URL like:
```python
/files/{file_path:path}
```
In this case, the name of the parameter is `file_path`, and the last part, `:path`, tells it that the parameter should match any path.

So, you can use it with:
```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```
<br>

## Query Parameters
Query parameters are a way to pass additional data to your API endpoints in the URL after a `?`. These parameters are key-value pairs separated by `&` and are not part of the main path of the endpoint.
```python
# Query Parameters with default values
@app.get("/items/{book_id}")
async def read_item(book_id: int, b_name: str = "ML", price: int = 1000):
    return {f"Book name = {b_name}" : f"Price = {price}"}
```
```console
http://127.0.0.1:8000/items/3?b_name=DL&price=2000
```
### Defaults query parameters
As query parameters are not a fixed part of a path, they can be `optional` and can have `default` values.

In the example above they have `default` values of b_name=ML and price=1000.

### Optional query parameters
```python
from typing import Union

@app.get("/items/{book_id}")
async def read_item(book_id: int, b_name: str = "ML", price: Union[int, None] = None):
    return {f"Book name = {b_name}" : f"Price = {price}"}
```
In this case, the function parameter `price` will be `optional`, and will be `None` by default.

### Query parameter type conversion
You can also declare bool types, and they will be converted:
```python
from typing import Union

@app.get("/items/{book_id}")
async def read_item(book_id: int, b_name: str = "ML", price: Union[int, None] = None, latest: bool = False):

    item_return = {f"Book name = {b_name}" : f"Price = {price}"}

    if latest:
        item_return.add({"Message": "This is the latest version."})

    return item
```
In this case, if you go to:
```console
http://127.0.0.1:8000/items/3?b_name=ML&price=2000&latest=1

http://127.0.0.1:8000/items/3?b_name=ML&price=2000&latest=True

http://127.0.0.1:8000/items/3?b_name=ML&price=2000&latest=true

http://127.0.0.1:8000/items/3?b_name=ML&price=2000&latest=on

http://127.0.0.1:8000/items/3?b_name=ML&price=2000&latest=yes
```
or any other case variation (uppercase, first letter in uppercase, etc), your function will see the parameter latest with a bool value of `True`. Otherwise as False.

### Multiple path and query parameters
You can declare multiple path parameters and query parameters at the same time, FastAPI knows which is which.

And you don't have to declare them in any specific order.

They will be detected by name:
```python
@app.get("/users/{user_id}/items/{item_id}")
```

### Required query parameters
When you declare a default value for non-path parameters (for now, we have only seen query parameters), then it is not required.

If you don't want to add a specific value but just make it optional, set the default as `None`.

But when you want to make a query parameter required, you can just not declare any default value:
```python
@app.get("/items/{book_id}")
async def read_item(book_id: int, b_name: str):
    return {"Book name" : b_name}
```
Without adding the required parameters, you will see an error like:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "b_name",
      ],
      "msg": "Field required",
      "input": null,
      "url": "https://errors.pydantic.dev/2.1/v/missing"
    }
  ]
}
```

And of course, you can define `some` parameters as `required`, some as having a `default` value, and some entirely `optional`:

```python
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    return
```

