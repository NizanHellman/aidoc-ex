from src.storage import LocalStorage
import os
import json
import yaml
import numpy as np
import csv


class SomeClass:
    def __init__(self, text: str, number: float):
        self.text = text
        self.number = number


def test_local_storage():
    storage = LocalStorage()
    for i in range(3):
        storage.save(i, SomeClass(chr(i), i))
    assert storage.count() == 3
    assert not storage.exists(4)
    assert storage.get(2).number + 1 == 3


def test_json_local_storage():
    json_content = {
        "name": "test",
        "value": 42,
        "nested": {"key": "value"}
    }
    
    # Save JSON to a file
    with open("test_data.json", "w") as f:
        json.dump(json_content, f)
    
    storage = LocalStorage()
    storage.save("json_key", "test_data.json")
    
    loaded_data = storage.get("json_key")
    assert loaded_data["name"] == "test"
    assert loaded_data["value"] == 42
    assert loaded_data["nested"]["key"] == "value"
    
    os.remove("test_data.json")


def test_yaml_local_storage():
    yaml_content = {
        'name': 'test',
        'values': [1, 2, 3],
        'nested': {'key': 'value'}
    }
    
    with open("test_data.yaml", "w") as f:
        yaml.dump(yaml_content, f)
    
    storage = LocalStorage()
    storage.save("yaml_key", "test_data.yaml")
    
    loaded_data = storage.get("yaml_key")
    assert loaded_data["name"] == "test"
    assert loaded_data["values"] == [1, 2, 3]
    assert loaded_data["nested"]["key"] == "value"
    
    os.remove("test_data.yaml")


def test_csv_local_storage():
    csv_content = [
        ["name", "age", "city"],
        ["Nizan", "33", "Mattan"],
        ["Noa", "33", "London"]
    ]
    
    with open("test_data.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_content)
    
    storage = LocalStorage()
    storage.save("csv_key", "test_data.csv")
    
    loaded_data = storage.get("csv_key")
    assert loaded_data[0] == ["name", "age", "city"]
    assert loaded_data[1] == ["Nizan", "33", "Mattan"]
    
    os.remove("test_data.csv")


def test_numpy_local_storage():
    array_data = np.array([[1, 2, 3], [4, 5, 6]])
    np.save("test_data.npy", array_data)
    
    storage = LocalStorage()
    storage.save("numpy_key", "test_data.npy")
    
    loaded_data = storage.get("numpy_key")
    assert np.array_equal(loaded_data, array_data)
    
    os.remove("test_data.npy")

