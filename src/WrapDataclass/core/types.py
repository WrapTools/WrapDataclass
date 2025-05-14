# core/types.py
"""
Type aliases for internal use in WrapDataclass.

Defines T for use in class method type hints involving BaseModel subclasses.
"""

from typing import TypeVar
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

T = TypeVar("T", bound="BaseModel")
