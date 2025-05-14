# core/helpers.py
"""
Helper functions for dataclass introspection and type resolution.
Includes utility functions to handle nested and optional dataclass fields.
"""

from dataclasses import fields, is_dataclass
from typing import Any, Union, get_args
import logging

# Logger Configuration
logger = logging.getLogger(__name__)


def get_dataclass_fields(obj: Any):
    """Return the fields of a dataclass, from instance or class."""
    return fields(obj.__class__) if not is_dataclass(obj) else fields(obj)

def is_dataclass_type(t: Any) -> bool:
    """Check if a type is a dataclass."""
    return isinstance(t, type) and is_dataclass(t)

def is_list_of_dataclass(t: Any) -> bool:
    """Determine whether a type is a list of dataclass instances."""
    origin = getattr(t, "__origin__", None)
    args = getattr(t, "__args__", [])

    # Unwrap Optional[List[T]] or Union[List[T], None]
    if origin is Union:
        for arg in args:
            if is_list_of_dataclass(arg):
                return True
        return False
    return origin is list and args and is_dataclass_type(args[0])


def resolve_dataclass_type(t: Any) -> Any:
    """Extract the dataclass type from Optional, Union, or List containers."""
    if getattr(t, "__origin__", None) is Union:
        for arg in get_args(t):
            if is_dataclass_type(arg):
                return arg
    return t

def get_list_inner_type(t: Any) -> Any:
    """Extract the inner type from a List[T] or Optional[List[T]]."""
    if getattr(t, "__origin__", None) is Union:
        for arg in get_args(t):
            inner = get_list_inner_type(arg)
            if inner:
                return inner
        return None

    if getattr(t, "__origin__", None) is list:
        return t.__args__[0]
    return None
