from typing import Any, List
import json
import yaml
import pathlib
import csv
import numpy as np


class StorageStrategy:
    def save(self, source_path: pathlib.Path, dest_path: pathlib.Path) -> None:
        raise NotImplementedError

    def load(self, file_path: pathlib.Path) -> Any:
        raise NotImplementedError

    @classmethod
    def can_handle(cls, file_path: pathlib.Path) -> bool:
        raise NotImplementedError


class JsonStrategy(StorageStrategy):
    @classmethod
    def can_handle(cls, file_path: pathlib.Path) -> bool:
        return file_path.suffix == '.json'

    def save(self, source_path: pathlib.Path, dest_path: pathlib.Path) -> None:
        with open(source_path, 'r') as src, open(dest_path, 'w') as dst:
            json.dump(json.load(src), dst)

    def load(self, file_path: pathlib.Path) -> Any:
        with open(file_path, 'r') as f:
            return json.load(f)


class YamlStrategy(StorageStrategy):
    @classmethod
    def can_handle(cls, file_path: pathlib.Path) -> bool:
        return file_path.suffix in ['.yaml', '.yml']

    def save(self, source_path: pathlib.Path, dest_path: pathlib.Path) -> None:
        with open(source_path, 'r') as src, open(dest_path, 'w') as dst:
            yaml.dump(yaml.safe_load(src), dst)

    def load(self, file_path: pathlib.Path) -> Any:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)


class NumpyStrategy(StorageStrategy):
    @classmethod
    def can_handle(cls, file_path: pathlib.Path) -> bool:
        return file_path.suffix == '.npy'

    def save(self, source_path: pathlib.Path, dest_path: pathlib.Path) -> None:
        array_data = np.load(source_path)
        np.save(dest_path, array_data)

    def load(self, file_path: pathlib.Path) -> np.ndarray:
        return np.load(file_path)


class CsvStrategy(StorageStrategy):
    @classmethod
    def can_handle(cls, file_path: pathlib.Path) -> bool:
        return file_path.suffix == '.csv'

    def save(self, source_path: pathlib.Path, dest_path: pathlib.Path) -> None:
        with open(source_path, 'r', newline='') as src, open(dest_path, 'w', newline='') as dst:
            writer = csv.writer(dst)
            reader = csv.reader(src)
            writer.writerows(reader)

    def load(self, file_path: pathlib.Path) -> List[List[str]]:
        with open(file_path, 'r', newline='') as f:
            return list(csv.reader(f))


class UnknownFileTypeError(Exception):
    """Raised when no strategy is found for a file type"""
    def __init__(self, file_path: pathlib.Path):
        self.file_path = file_path
        self.message = f"No strategy found for file type: {file_path.suffix}"
        super().__init__(self.message)


class StorageStrategyFactory:
    """Factory for creating storage strategies"""
    def __init__(self):
        self.strategies = [
            JsonStrategy(),
            YamlStrategy(),
            NumpyStrategy(),
            CsvStrategy(),
        ]

    def get_strategy(self, file_path: pathlib.Path) -> StorageStrategy:
        for strategy in self.strategies:
            if strategy.can_handle(file_path):
                return strategy
        raise UnknownFileTypeError(file_path)
