# Pydantic

>Pydantic is a data validation and settings management library for Python, deeply integrated into FastAPI to handle request and response data. 

It uses Python's type hints to validate, serialize, and deserialize data efficiently. 

## 1. Core Concepts
Pydantic models are Python classes that inherit from `BaseModel`. These models:

* Define the structure of data (schemas)
* Validate data against the specified types
* Serialize and deserialize data automatically

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True  # Default value

user_data = {"id": 1, "name": "Harry", "email": "harry@example.com"}
user = User(**user_data)  # Instantiate the model
print(user.dict())        # Convert model to dictionary
```

## 2. Pydantic with FastAPI
### Request Validation
Pydantic models validate incoming data in FastAPI requests.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users/")
def create_user(user: User):
    return {"message": f"User {user.name} created successfully!"}
```
* If invalid data is sent, FastAPI automatically returns a 422 Unprocessable Entity error with detailed validation errors.

### Response Validation
You can use Pydantic models to define response data.
```python
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    return {"name": "Harry", "email": "harry@example.com", "age": 25}  # Must match `User` schema
```

## 3. Advanced Features of Pydantic
### Field Validations
Use `Field` to enforce constraints on fields (e.g., minimum/maximum lengths, regex patterns).

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, le=120)  # greater than 0, less than or equal to 120
    email: str
```

### Custom Validators
Define custom validation logic using `@validator`.
from pydantic import BaseModel, EmailStr, validator

```python
class User(BaseModel):
    name: str
    email: EmailStr

    @validator("name")
    def validate_name(cls, value):
        if not value.isalpha():
            raise ValueError("Name must only contain letters")
        return value
```

## 4. Nested Models
Pydantic supports nesting models, allowing hierarchical data validation.

```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    email: str
    address: Address
```
JSON Example:
```json
{
  "name": "Harry",
  "email": "harry@example.com",
  "address": {
    "street": "123 Main St",
    "city": "Mumbai",
    "zip_code": "400001"
  }
}
```
