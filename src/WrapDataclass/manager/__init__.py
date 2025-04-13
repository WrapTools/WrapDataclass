# __init__.py
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
