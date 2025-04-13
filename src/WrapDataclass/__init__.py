# __init__.py

from .base import BaseModel
from .mixin_dict import DictMixin
from .mixin_file import FileMixin
from .mixin_dictlike import DictLikeMixin
from .helpers import resolve_dataclass_type, get_list_inner_type

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
