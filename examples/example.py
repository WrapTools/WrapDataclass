# example.py

# Configure Logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format = '%(name)s - %(levelname)s - %(message)s (line: %(lineno)d)',
    handlers=[
        logging.StreamHandler(),  # Log to console
        # logging.FileHandler('app.log')  # Log to file
    ]
)

from WrapDataclass import BaseModel

# Example
from dataclasses import dataclass
from typing import Optional, List

# Assume BaseModel is imported and working

@dataclass
class Tag(BaseModel):
    label: str
    importance: int = 1

@dataclass
class Metadata(BaseModel):
    author: str
    created: str
    tags: Optional[List[Tag]] = None

@dataclass
class SubItem(BaseModel):
    name: str
    value: Optional[int] = None

@dataclass
class MainItem(BaseModel):
    title: str
    description: Optional[str] = None
    sub: Optional[SubItem] = None
    metadata: Optional[Metadata] = None
    flags: Optional[List[str]] = None

# Construct a full example
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

# Save to JSON
main.to_json("example.json", app_name="DemoApp", data_version="2.1")

# Load from JSON
loaded = MainItem.from_json("example.json", require_type="MainItem")

# Print main fields
print(f"Title: {loaded.title}")
print(f"Description: {loaded.description}")
print(f"Sub name: {loaded.sub.name}")
print(f"First tag: {loaded.metadata.tags[0].label}")

# Dict-style access
print(loaded["title"])      # -> Demo Document
loaded["title"] = "Updated Title"
print(loaded.title)         # -> Updated Title

# Iterate fields like a dict
print("\nFields:")
for key in loaded.keys():
    print(f" - {key}")

print("\nValues:")
for val in loaded.values():
    print(f" - {val}")

print("\nItems:")
for key, val in loaded.items():
    print(f" - {key}: {val}")

# Export to dictionary
as_dict = loaded.to_dict()
print("\nDict Export (clean):")
print(as_dict)

# Print with Header
item, header = MainItem.from_json_with_header("example.json")
print("\nHeader information:")
print(item.title)
print(header["data_version"])

print("\nIterating over model (keys):")
for key in loaded:
    print(f"{key} -> {loaded[key]}")


