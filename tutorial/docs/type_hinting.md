# Type Hinting

Type hinting in Python allows you to explicitly declare the types of variables, function parameters, and return values. 

It improves code readability, catches type-related bugs during development.

## Basic Built-In Types
These include the standard Python data types:

* `int`: Integers.
* `float`: Floating-point numbers.
* `bool`: Boolean values (True/False).
* `str`: Strings.
* `None`: Represents no value (used as Optional in type hints).

```python
def add_numbers(a: int, b: int) -> int:
    return a + b

x: int = 10
y: float = 3.14
name: str = "Harry"
is_valid: bool = True
```

## Collections and Generics

* `list[T]`: A list containing elements of type T.
* `tuple[T1, T2, ...]`: A tuple with fixed-length and element types.
* `set[T]`: A set containing elements of type T.
* `dict[K, V]`: A dictionary with keys of type K and values of type V.

```python
numbers: ltst[int] = [1, 2, 3]
coordinates: Tuple[float, float] = (12.5, 45.7)
unique_items: set[str] = {"apple", "banana"}
person: dict[str, int] = {"age": 30, "height": 170}
```

## Optional and Union

`Union[T1, T2, ...]`: You can declare that a variable can be any of several types, for example, an int or a str.
In `Python 3.10` there's also a new syntax where you can put the possible types separated by a vertical bar (`|`).

```python
def process_item(item: int | str):
    print(item)
```

---

`Optional[T]`: Specifies that a value can be of type T or None.
```python
from typing import Optional

def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
```

> Note: `Optional[T]` is equivalent to `Union[T, None]`.
