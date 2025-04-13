# mixin_dictlike.py

from typing import Any
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from .helpers import get_dataclass_fields


# DictLikeMixin
class DictLikeMixin:
    """Enables dict-like access to dataclass fields (getitem, keys, etc.)."""
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        return setattr(self, key, value)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def __iter__(self):
        return iter(self.keys())

    def keys(self):
        return (f.name for f in get_dataclass_fields(self))

    def values(self):
        return (getattr(self, f.name) for f in get_dataclass_fields(self))

    def items(self):
        return ((f.name, getattr(self, f.name)) for f in get_dataclass_fields(self))