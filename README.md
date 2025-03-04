# aidoc-ex

# Local Storage with Strategy Pattern

A simple Python storage system that demonstrates the Strategy pattern for handling different data types.

## Overview

This project implements a local storage system that can save and retrieve different types of data using appropriate serialization strategies. The system uses the Strategy pattern to handle different data formats.

## Features

- Save and retrieve different types of data:
  - JSON-serializable data (dictionaries and lists)
  - NumPy arrays (.npy files)
  - CSV data (lists of lists)
  - Custom objects (SomeClass example)
- Extensible design using the Strategy pattern
- Simple key-value storage interface
- Persistent storage with automatic index management
- Type-specific serialization strategies
- Automatic file extension handling

## Usage

```python
from storage import LocalStorage

# Initialize storage
storage = LocalStorage("example_storage")

# Store data
user = {
    "name": "Nizan",
    "age": 33,
    "hobbies": ["coding", "gaming"]
}
storage.save("user", user)

# Retrieve data
loaded_user = storage.get("user")
print(f"Name: {loaded_user['name']}")
```

## Project Structure

```
src/
├── __init__.py
├── storage.py     # Main storage implementation
├── strategy.py    # Strategy pattern implementation
└── main.py        # Example usage
```

## Running the Example
```bash
python -m src.main
```
## Running Tests

```bash
pytest tests/
```

# Design Patterns Used

- Strategy Pattern: For handling different data types and serialization formats
- Factory Pattern: For creating appropriate strategies based on data type

## Extensibility

The system is designed to be easily extensible in two ways:

### 1. Adding New Data Types

To add support for a new data type:
1. Create a new strategy class that implements the `StorageStrategy` interface
2. Add the strategy to the `StorageStrategyFactory`

Example:
```python
class XmlStrategy(StorageStrategy):
    @classmethod
    def can_handle(cls, source: Any) -> bool:
        return isinstance(source, XmlElement)

    def save(self, source: Any, dest_path: pathlib.Path) -> None:
        # Implementation for saving XML
```

### 2. Adding New Storage Backends

To add a new storage backend (e.g., S3, Redis):
1. Create a new class that inherits from `BaseStorage`
2. Implement the required methods (`save`, `get`, `exists`, `count`)

Example:
```python
class S3Storage(BaseStorage):
    def __init__(self, bucket_name: str):
        super().__init__()
        self.bucket = bucket_name
        self.strategy_factory = StorageStrategyFactory()

    def save(self, key: Any, data: Any) -> None:
        # Implementation for S3 storage
```

The strategy system will work with any storage backend that implements the `BaseStorage` interface.


