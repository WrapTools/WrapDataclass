# base_manager

from pathlib import Path
from typing import Type, TypeVar, Generic
import logging
import json
from ..core.base import BaseModel

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)

class BaseManager(Generic[T]):
    def __init__(self, model_type: Type[T], directory: Path):
        self.model_type = model_type
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, obj: T, name: str = None, *, app_name: str = "", version: str = "") -> None:
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
        path = self.directory / f"{name}.json"
        return self.model_type.from_json(path, require_type=self.model_type.__name__)

    def exists(self, name: str) -> bool:
        return (self.directory / f"{name}.json").exists()

    def delete(self, name: str) -> None:
        path = self.directory / f"{name}.json"
        if path.exists():
            path.unlink()

    def get_or_create(self, obj: T, name: str = None, **save_kwargs) -> T:
        path = self.directory / f"{name or obj.id}.json"
        if not path.exists():
            self.save(obj, name=name, **save_kwargs)
        return self.load(name or obj.id)

