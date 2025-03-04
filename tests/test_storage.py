import numpy as np
import pytest
from src.storage import LocalStorage
from src.strategy import UnknownTypeError


@pytest.fixture
def storage(tmp_path):
    """Create a LocalStorage instance using a temporary directory"""
    return LocalStorage(str(tmp_path))


# def test_local_storage(storage):
#     for i in range(3):
#         storage.save(i, SomeClass(chr(i), i))
#     assert storage.count() == 3
#     assert not storage.exists(4)
#     assert storage.get(2).number + 1 == 3


def test_json_local_storage(storage):
    json_content = {
        "name": "test",
        "value": 42,
        "nested": {"key": "value"}
    }

    storage.save("json_key", json_content)

    loaded_data = storage.get("json_key")
    assert loaded_data["name"] == "test"
    assert loaded_data["value"] == 42
    assert loaded_data["nested"]["key"] == "value"


def test_yaml_local_storage(storage):
    yaml_content = {
        'name': 'test',
        'values': [1, 2, 3],
        'nested': {'key': 'value'}
    }

    storage.save("yaml_key", yaml_content)

    loaded_data = storage.get("yaml_key")
    assert loaded_data["name"] == "test"
    assert loaded_data["values"] == [1, 2, 3]
    assert loaded_data["nested"]["key"] == "value"


def test_csv_local_storage(storage):
    csv_content = [
        ["name", "age", "city"],
        ["Nizan", "33", "Mattan"],
        ["Noa", "33", "London"]
    ]

    storage.save("csv_key", csv_content)

    loaded_data = storage.get("csv_key")
    assert loaded_data[0] == ["name", "age", "city"]
    assert loaded_data[1] == ["Nizan", "33", "Mattan"]


def test_numpy_local_storage(storage):
    array_data = np.array([[1, 2, 3], [4, 5, 6]])

    storage.save("numpy_key", array_data)

    loaded_data = storage.get("numpy_key")
    assert np.array_equal(loaded_data, array_data)


def test_unknown_type(storage):
    class UnknownClass:
        pass

    with pytest.raises(UnknownTypeError) as exc_info:
        storage.save("test_key", UnknownClass())
    assert "UnknownClass" in str(exc_info.value)


def test_save_and_get_supported_types(storage):
    # Test dictionary
    dict_data = {"key": "value"}
    storage.save("dict_key", dict_data)
    assert storage.get("dict_key") == dict_data
    
    # Test list
    list_data = [1, 2, 3]
    storage.save("list_key", list_data)
    assert storage.get("list_key") == list_data

