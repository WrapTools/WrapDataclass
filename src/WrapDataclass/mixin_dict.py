# mixin_dict.py

from dataclasses import is_dataclass
from typing import Type, TypeVar, get_type_hints, cast
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from .helpers import get_dataclass_fields, resolve_dataclass_type, is_dataclass_type, is_list_of_dataclass, get_list_inner_type
from .types import T


# DictMixin
class DictMixin:
    """Provides to_dict() and from_dict() for nested dataclass conversion."""
    def to_dict(self, skip_none: bool = True) -> dict:
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