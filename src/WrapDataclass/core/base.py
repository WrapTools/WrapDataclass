# base.py

from dataclasses import dataclass
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from .mixin_dictlike import DictLikeMixin
from .mixin_file import FileMixin


@dataclass
class BaseModel(DictLikeMixin, FileMixin):
    """Unified base class with dict, JSON, and dict-like behavior."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_dict(skip_none=True)})"