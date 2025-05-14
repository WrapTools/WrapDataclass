# basic_model_demo.py
"""
Demonstrates core usage of WrapDataclass BaseModel:
- Nested dataclasses
- Dict-style access
- Optional and list fields
- JSON save/load with header
- Header inspection
"""

# Configure Logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s (line: %(lineno)d)',
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler('app.log')
    ]
)

from WrapDataclass import BaseModel

from dataclasses import dataclass
from typing import Optional, List

# === Original Models ===

@dataclass
class Tag(BaseModel):
    """Single tag with importance level."""
    label: str
    importance: int = 1

@dataclass
class Metadata(BaseModel):
    """Metadata including author, created date, and tags."""
    author: str
    created: str
    tags: Optional[List[Tag]] = None

@dataclass
class SubItem(BaseModel):
    """Optional nested sub-structure."""
    name: str
    value: Optional[int] = None

@dataclass
class MainItem(BaseModel):
    """Main document with optional metadata and sub-objects."""
    title: str
    description: Optional[str] = None
    sub: Optional[SubItem] = None
    metadata: Optional[Metadata] = None
    flags: Optional[List[str]] = None

# === Multi-Section Models ===

@dataclass
class Summary(BaseModel):
    highlights: list[str]
    conclusion: str

@dataclass
class Evaluation(BaseModel):
    score: float
    notes: str

@dataclass
class DocumentWithSections(BaseModel):
    summary: Summary
    evaluation: Evaluation

# === Serialize and Load Example ===

main = MainItem(
    title="Demo Document",
    description="This is a test of the BaseModel system.",
    sub=SubItem(name="Nested Element", value=42),
    metadata=Metadata(
        author="Alice",
        created="2024-04-12",
        tags=[Tag(label="example"), Tag(label="test", importance=2)]
    ),
    flags=["important", "review"]
)

main.to_json("example.json", app_name="DemoApp", data_version="2.1")
loaded = MainItem.from_json("example.json", require_type="MainItem")

# === Access Tests ===
print(f"Title: {loaded.title}")
print(f"Description: {loaded.description}")
print(f"Sub name: {loaded.sub.name}")
print(f"First tag: {loaded.metadata.tags[0].label}")

# Dict-style field access
print(loaded["title"])      # -> Demo Document
loaded["title"] = "Updated Title"
print(loaded.title)         # -> Updated Title

# Keys, values, and items
print("\nFields:")
for key in loaded.keys():
    print(f" - {key}")

print("\nValues:")
for val in loaded.values():
    print(f" - {val}")

print("\nItems:")
for key, val in loaded.items():
    print(f" - {key}: {val}")

# Convert to dict
as_dict = loaded.to_dict()
print("\nDict Export (clean):")
print(as_dict)

# Load with header info
item, header = MainItem.from_json_with_header("example.json")
print("\nHeader information:")
print(item.title)
print(header["data_version"])

# Iterating with __getitem__
print("\nIterating over model (keys):")
for key in loaded:
    print(f"{key} -> {loaded[key]}")
