# core/mixin_dict.py
"""
DictMixin for serialization of dataclasses.

Provides `to_dict` and `from_dict` methods for serializing dataclass instances,
including nested dataclasses and lists of dataclasses.
"""

from dataclasses import is_dataclass
from typing import Type, TypeVar, get_type_hints, cast
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from .helpers import get_dataclass_fields, resolve_dataclass_type, is_dataclass_type, is_list_of_dataclass, get_list_inner_type
from .types import T


# DictMixin
class DictMixin:
    """Serialization mixin for dataclasses.
       Supports conversion to and from dictionaries, including nested structures.
    """
    def to_dict(self, skip_none: bool = True) -> dict:
        """Convert the dataclass instance to a dictionary.
                Args:
                    skip_none (bool): If True, omit fields with None values.
                Returns:
                    dict: Dictionary representation of the dataclass.
        """
        result = {}
        for f in get_dataclass_fields(self):
            value = getattr(self, f.name)
            if value is None and skip_none:
                continue
            elif is_dataclass(value):
                result[f.name] = cast(DictMixin, value).to_dict(skip_none=skip_none)
            elif isinstance(value, list):
                result[f.name] = [
                    item.to_dict(skip_none=skip_none) if is_dataclass(item) else item
                    for item in value
                    if item is not None or not skip_none
                ]
            else:
                result[f.name] = value
        return result

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """Reconstruct a dataclass instance from a dictionary.
                Args:
                    data (dict): Dictionary to load values from.
                Returns:
                    An instance of the dataclass.
        """
        kwargs = {}
        type_hints = get_type_hints(cls)

        for key, val in data.items():
            field_type = resolve_dataclass_type(type_hints.get(key))
            if is_dataclass_type(field_type) and isinstance(val, dict):
                kwargs[key] = field_type.from_dict(val)
            elif is_list_of_dataclass(field_type) and isinstance(val, list):
                sub_type = get_list_inner_type(type_hints.get(key))
                kwargs[key] = [
                    sub_type.from_dict(i) if isinstance(i, dict) else i for i in val
                ]
            else:
                kwargs[key] = val

        return cast(Type[T], cls)(**kwargs)
