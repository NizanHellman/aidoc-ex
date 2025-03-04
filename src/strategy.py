from typing import Any
import json
import yaml
import pathlib


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


class StorageStrategyFactory:
    """Factory for creating storage strategies"""
    def __init__(self):
        self.strategies = [
            JsonStrategy(),
            YamlStrategy(),
            # Add more strategies here
        ]

    def get_strategy(self, file_path: pathlib.Path) -> StorageStrategy:
        for strategy in self.strategies:
            if strategy.can_handle(file_path):
                return strategy
        raise ValueError(f"No strategy found for file type: {file_path.suffix}")
