# manager/base_record.py
"""
Record classes for WrapDataclass manager module.

Includes base dataclass record types with ID support and flexible content fields.
"""

from dataclasses import dataclass, field
import uuid
from ..core.base import BaseModel


@dataclass
class BaseRecord(BaseModel):
    """A base record requiring a user-provided ID.
    Use this when IDs must be externally controlled (e.g., from a database or user input).
    """
    id: str


@dataclass(kw_only=True)
class AutoIDRecord(BaseModel):
    """A base record that automatically generates a UUID string as its ID.
    Ideal for records that need guaranteed uniqueness without requiring caller input.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass(kw_only=True)
class FlexibleRecord(BaseModel):
    """A flexible base record with UUID ID, title, and body fields.
    Useful for note-taking, text storage, or lightweight document records.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    body: str
