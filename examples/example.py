# example.py

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

# === MainItem Example ===

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

print(f"Title: {loaded.title}")
print(f"Description: {loaded.description}")
print(f"Sub name: {loaded.sub.name}")
print(f"First tag: {loaded.metadata.tags[0].label}")

print(loaded["title"])      # -> Demo Document
loaded["title"] = "Updated Title"
print(loaded.title)         # -> Updated Title

print("\nFields:")
for key in loaded.keys():
    print(f" - {key}")

print("\nValues:")
for val in loaded.values():
    print(f" - {val}")

print("\nItems:")
for key, val in loaded.items():
    print(f" - {key}: {val}")

as_dict = loaded.to_dict()
print("\nDict Export (clean):")
print(as_dict)

item, header = MainItem.from_json_with_header("example.json")
print("\nHeader information:")
print(item.title)
print(header["data_version"])

print("\nIterating over model (keys):")
for key in loaded:
    print(f"{key} -> {loaded[key]}")

# === Multi-Section Example ===

multi = DocumentWithSections(
    summary=Summary(
        highlights=["Concise", "Covers edge cases", "Good test coverage"],
        conclusion="Ready for deployment"
    ),
    evaluation=Evaluation(
        score=9.5,
        notes="Excellent structure and extensibility."
    )
)

multi.to_json("multi_section.json", app_name="WrapTools", data_version="3.0")

# Load and display
loaded_multi = DocumentWithSections.from_json("multi_section.json")
print("\n[MultiSectionModel]")
print("Highlights:", loaded_multi.summary.highlights)
print("Evaluation Score:", loaded_multi.evaluation.score)

loaded_multi, meta = DocumentWithSections.from_json_with_header("multi_section.json")
print("Loaded with header:", meta["app_name"], meta["data_version"])

