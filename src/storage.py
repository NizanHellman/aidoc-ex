import csv
from typing import Any, Dict
import json
import os
import pathlib

import numpy as np
import yaml

from .strategy import StorageStrategyFactory


class BaseStorage:
    def __init__(self):
        pass

    def save(self, key: Any, data: Any) -> None:
        """Save data with the given key"""
        raise NotImplementedError

    def get(self, key: Any) -> Any:
        """Retrieve data for the given key"""
        raise NotImplementedError

    def count(self) -> int:
        """Return the number of stored items"""
        raise NotImplementedError

    def exists(self, key: Any) -> bool:
        """Check if a key exists in storage"""
        raise NotImplementedError


class LocalStorage(BaseStorage):
    def __init__(self, storage_dir: str = "storage"):
        super().__init__()
        self.storage_dir = pathlib.Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_dir / "index.json"
        self.strategy_factory = StorageStrategyFactory()
        self._load_index()

    def _load_index(self):
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self._index = json.load(f)
        else:
            self._index = {}
            self._save_index()

    def _save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump(self._index, f)

    def _get_file_path(self, key: str) -> pathlib.Path:
        return self.storage_dir / f"{key}"

    def save(self, key: Any, data: Any) -> None:
        """Save data to a file in the storage directory"""
        file_path = self._get_file_path(str(key))
        
        if isinstance(data, str) and os.path.exists(data):
            # If data is a file path, copy the file to storage
            source_path = pathlib.Path(data)
            dest_path = file_path.with_suffix(source_path.suffix)
            
            try:
                strategy = self.strategy_factory.get_strategy(source_path)
                strategy.save(source_path, dest_path)
            except ValueError:
                # Fallback for unknown file types
                with open(source_path, 'rb') as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())
                    
            self._index[str(key)] = str(dest_path)
        else:
            # For other types, serialize to JSON
            dest_path = file_path.with_suffix('.json')
            with open(dest_path, 'w') as f:
                json.dump(data, f)
            self._index[str(key)] = str(dest_path)
        
        self._save_index()

    def get(self, key: Any) -> Any:
        """Retrieve data from storage"""
        if not self.exists(key):
            return None
            
        file_path = pathlib.Path(self._index[str(key)])
        if not file_path.exists():
            return None
            
        try:
            strategy = self.strategy_factory.get_strategy(file_path)
            return strategy.load(file_path)
        except ValueError:
            # Fallback for unknown file types
            with open(file_path, 'rb') as f:
                return f.read()

    def count(self) -> int:
        return len(self._index)

    def exists(self, key: Any) -> bool:
        return str(key) in self._index


