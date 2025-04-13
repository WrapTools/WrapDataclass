from dataclasses import dataclass, field
import uuid
from ..core.base import BaseModel


@dataclass
class BaseRecord(BaseModel):
    """A base record with a required string ID (must be passed explicitly)."""
    id: str


@dataclass(kw_only=True)
class AutoIDRecord(BaseModel):
    """A base record with an auto-generated UUID if no ID is passed."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass(kw_only=True)
class FlexibleRecord(BaseModel):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    body: str
