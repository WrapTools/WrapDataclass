# core/mixin_dictlike.py
"""
DictLikeMixin for attribute-style dictionary access.
Allows dataclass fields to be accessed using dictionary-like syntax.
"""

from typing import Any
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from .helpers import get_dataclass_fields


# DictLikeMixin
class DictLikeMixin:
    """Enables dictionary-style access for dataclass fields (e.g., obj['field'])."""
    def __getitem__(self, key: str) -> Any:
        """Retrieve a field value via dict-style access."""
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a field value via dict-style access."""
        return setattr(self, key, value)

    def __contains__(self, key: str) -> bool:
        """Check if a field exists."""
        return hasattr(self, key)

    def __iter__(self):
        """Iterate over the field names."""
        return iter(self.keys())

    def keys(self):
        """Return an iterator over field names."""
        return (f.name for f in get_dataclass_fields(self))

    def values(self):
        """Return an iterator over field values."""
        return (getattr(self, f.name) for f in get_dataclass_fields(self))

    def items(self):
        """Return an iterator of (field name, value) pairs."""
        return ((f.name, getattr(self, f.name)) for f in get_dataclass_fields(self))
