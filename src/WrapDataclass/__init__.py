# __init__.py

from .core.base import BaseModel
from .core.mixin_dict import DictMixin
from .core.mixin_file import FileMixin
from .core.mixin_dictlike import DictLikeMixin
from .core.helpers import resolve_dataclass_type, get_list_inner_type


import logging

# Create a logger for your library
logger = logging.getLogger(__name__)
# logger.addHandler(logging.NullHandler())

__all__ = [
    "BaseModel",
    "DictMixin",
    "FileMixin",
    "DictLikeMixin",
    "resolve_dataclass_type",
    "get_list_inner_type",
]
