# core/base.py
"""
BaseModel definition for WrapDataclass.
Combines DictLike, Dict, and File mixins into a single serializable dataclass.
"""

from dataclasses import dataclass
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from .mixin_dictlike import DictLikeMixin
from .mixin_file import FileMixin


@dataclass
class BaseModel(DictLikeMixin, FileMixin):
    """Base class for serializable dataclasses.

    Combines dict-like access (`obj['key']`), dictionary serialization (`to_dict`, `from_dict`),
    and file-based JSON persistence (`to_json`, `from_json`).
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_dict(skip_none=True)})"
