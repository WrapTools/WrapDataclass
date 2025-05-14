# manager/base_manager
"""
BaseManager for managing dataclass records as JSON files on disk.
Supports save/load/delete operations and automatic directory creation.
"""

from pathlib import Path
from typing import Type, TypeVar, Generic
import logging
import json
from ..core.base import BaseModel

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)

class BaseManager(Generic[T]):
    """Handles file-based persistence for dataclass instances using JSON files."""
    def __init__(self, model_type: Type[T], directory: Path):
        """
        Initialize the manager for a specific dataclass type.
        Args:
            model_type (Type[T]): The dataclass type this manager handles.
            directory (Path): The base directory where JSON files are stored.
        """
        self.model_type = model_type
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, obj: T, name: str = None, *, app_name: str = "", version: str = "") -> None:
        """
        Save a dataclass instance to a JSON file.
        Args:
            obj (T): The object to save.
            name (str): Optional override for the filename (defaults to `obj.id`).
            app_name (str): Application name to include in file header.
            version (str): Version string to include in file header.
        """
        name = name or getattr(obj, "id", None)
        if not name:
            raise ValueError("Object must have an 'id' or you must provide a name.")

        path = self.directory / f"{name}.json"
        obj.to_json(
            path,
            app_name=app_name or "WrapManager",
            data_version=version or "1.0",
            file_type=obj.__class__.__name__,
        )

    def load(self, name: str) -> T:
        """
        Load a dataclass instance from a JSON file by name.
        Args:
            name (str): Name of the file (without extension).
        Returns:
            T: An instance of the managed dataclass.
        """
        path = self.directory / f"{name}.json"
        return self.model_type.from_json(path, require_type=self.model_type.__name__)

    def exists(self, name: str) -> bool:
        """
        Check if a record file exists.
        Args:
            name (str): Name of the file (without extension).
        Returns:
            bool: True if file exists, False otherwise.
        """
        return (self.directory / f"{name}.json").exists()

    def delete(self, name: str) -> None:
        """
        Delete a record file.
        Args:
            name (str): Name of the file (without extension).
        """
        path = self.directory / f"{name}.json"
        if path.exists():
            path.unlink()

    def get_or_create(self, obj: T, name: str = None, **save_kwargs) -> T:
        """
        Load an existing record or create/save it if it doesn't exist.
        Args:
            obj (T): The object to save if no file is found.
            name (str): Optional override for the filename.
            **save_kwargs: Additional keyword arguments passed to `save`.
        Returns:
            T: The loaded or newly saved object.
        """
        path = self.directory / f"{name or obj.id}.json"
        if not path.exists():
            self.save(obj, name=name, **save_kwargs)
        return self.load(name or obj.id)
