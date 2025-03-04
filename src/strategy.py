from typing import Any, List
import json
import pathlib
import csv
import numpy as np


class StorageStrategy:
    def save(self, source: Any, dest_path: pathlib.Path) -> None:
        raise NotImplementedError

    def load(self, file_path: pathlib.Path) -> Any:
        raise NotImplementedError

    @classmethod
    def can_handle(cls, source: Any) -> bool:
        raise NotImplementedError

    @classmethod
    def handles_extension(cls) -> str:
        raise NotImplementedError


class JsonStrategy(StorageStrategy):
    @classmethod
    def can_handle(cls, source: Any) -> bool:
        return isinstance(source, (dict, list))

    @classmethod
    def handles_extension(cls) -> str:
        return '.json'

    def save(self, source: Any, dest_path: pathlib.Path) -> None:
        with open(dest_path, 'w') as f:
            json.dump(source, f)

    def load(self, file_path: pathlib.Path) -> Any:
        with open(file_path, 'r') as f:
            return json.load(f)


class NumpyStrategy(StorageStrategy):
    @classmethod
    def can_handle(cls, source: Any) -> bool:
        return isinstance(source, np.ndarray)

    @classmethod
    def handles_extension(cls) -> str:
        return '.npy'

    def save(self, source: np.ndarray, dest_path: pathlib.Path) -> None:
        np.save(dest_path, source)

    def load(self, file_path: pathlib.Path) -> np.ndarray:
        return np.load(file_path)


class CsvStrategy(StorageStrategy):
    @classmethod
    def can_handle(cls, source: Any) -> bool:
        return isinstance(source, list) and all(isinstance(row, list) for row in source)

    @classmethod
    def handles_extension(cls) -> str:
        return '.csv'

    def save(self, source: List[List[str]], dest_path: pathlib.Path) -> None:
        with open(dest_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(source)

    def load(self, file_path: pathlib.Path) -> List[List[str]]:
        with open(file_path, 'r', newline='') as f:
            return list(csv.reader(f))


class UnknownTypeError(Exception):
    """Raised when no strategy is found for a given type"""
    def __init__(self, obj: Any):
        self.obj = obj
        self.message = f"No strategy found for type: {type(obj).__name__}"
        super().__init__(self.message)


class StorageStrategyFactory:
    """Factory for creating storage strategies"""
    def __init__(self):
        self.strategies = [
            JsonStrategy(),
            NumpyStrategy(),
            CsvStrategy(),
        ]

    def get_strategy(self, source: Any) -> StorageStrategy:
        # When loading, use file extension to find strategy
        if isinstance(source, (str, pathlib.Path)):
            path = pathlib.Path(source)
            for strategy in self.strategies:
                if path.suffix == strategy.handles_extension():
                    return strategy
            raise UnknownTypeError(source)
        
        # When saving, use object type to find strategy
        for strategy in self.strategies:
            if strategy.can_handle(source):
                return strategy
        raise UnknownTypeError(source)
