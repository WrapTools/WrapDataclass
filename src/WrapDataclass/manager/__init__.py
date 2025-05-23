# manager/__init__.py
"""
Manager module for WrapDataclass.

Provides reusable manager and record classes for handling collections of dataclass-based records.
Useful for saving, loading, and managing structured JSON records on disk.
"""

import logging

# Create a logger for your library
logger = logging.getLogger(__name__)
# logger.addHandler(logging.NullHandler())

from .base_manager import BaseManager
from .base_record import BaseRecord, AutoIDRecord, FlexibleRecord

__all__ = [
    "BaseManager",
    "BaseRecord",
    "AutoIDRecord",
    "FlexibleRecord"
]
