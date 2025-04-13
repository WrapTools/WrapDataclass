# types.py

from typing import TypeVar
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

T = TypeVar("T", bound="BaseModel")
