# mixin_file.py

from typing import Type, TypeVar, TextIO
import json
from pathlib import Path
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from .mixin_dict import DictMixin
from .types import T

# FileMixin
class FileMixin(DictMixin):
    """Provides to_json() and from_json() with header support."""
    def to_json(
        self,
        path: Path | str,
        *,
        app_name: str,
        data_version: str,
        file_type: str = None,
        skip_none: bool = True
    ) -> None:
        path = Path(path)
        wrapper = {
            "header": {
                "app_name": app_name,
                "data_version": data_version,
                "file_type": file_type or self.__class__.__name__,
            },
            "data": self.to_dict(skip_none=skip_none),
        }

        with path.open("w", encoding="utf-8") as f:
            f_: TextIO = f
            json.dump(wrapper, f_, indent=2)

    @classmethod
    def from_json(cls: Type[T], path: Path | str, require_type: str = None) -> T:
        path = Path(path)
        try:
            with path.open("r", encoding="utf-8") as f:
                content = json.load(f)

            if not isinstance(content, dict):
                raise ValueError("Top-level JSON structure must be a dictionary")

            header = content.get("header")
            data = content.get("data")

            if not header or not data:
                raise ValueError("JSON file must contain 'header' and 'data' sections")

            if require_type and header.get("file_type") != require_type:
                raise ValueError(
                    f"Expected file_type '{require_type}', got '{header.get('file_type')}'"
                )

            return cls.from_dict(data)

        except (OSError, json.JSONDecodeError, KeyError, TypeError) as e:
            raise ValueError(f"Error loading JSON file '{path}': {e}")

    @classmethod
    def from_json_with_header(cls: Type[T], path: Path | str, require_type: str = None) -> tuple[T, dict]:
        path = Path(path)
        try:
            with path.open("r", encoding="utf-8") as f:
                content = json.load(f)

            if not isinstance(content, dict):
                raise ValueError("Top-level JSON structure must be a dictionary")

            header = content.get("header")
            data = content.get("data")

            if not header or not data:
                raise ValueError("JSON file must contain 'header' and 'data' sections")

            if require_type and header.get("file_type") != require_type:
                raise ValueError(
                    f"Expected file_type '{require_type}', got '{header.get('file_type')}'"
                )

            return cls.from_dict(data), header

        except (OSError, json.JSONDecodeError, KeyError, TypeError) as e:
            raise ValueError(f"Error loading JSON file '{path}': {e}")