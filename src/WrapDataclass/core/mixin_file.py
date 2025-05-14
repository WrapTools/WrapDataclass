# core/mixin_file.py
"""
FileMixin for loading and saving dataclass instances to JSON files.
Extends DictMixin with file read/write support using a standardized header.
"""

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
    """Provides JSON serialization/deserialization with header metadata."""
    def to_json(
        self,
        path: Path | str,
        *,
        app_name: str,
        data_version: str,
        file_type: str = None,
        skip_none: bool = True
    ) -> None:
        """Save the dataclass to a JSON file with header metadata.
                Args:
                    path (str | Path): Output file path.
                    app_name (str): Name of the application.
                    data_version (str): Version string for data format.
                    file_type (str): Optional file type name override.
                    skip_none (bool): Whether to skip fields with None values.
        """
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
        """Load an instance from a JSON file.
                Args:
                    path (str | Path): File to load.
                    require_type (str | None): Optional type check for header's file_type.
                Returns:
                    An instance of the dataclass.
        """
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
        """Load an instance and its metadata header from a JSON file.
                Returns:
                    tuple: (dataclass instance, header dictionary)
        """
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