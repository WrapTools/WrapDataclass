# cradle_to_grave.py
"""
Comprehensive usage example for WrapDataclass library.

Demonstrates how to:
- Define nested dataclass models
- Automatically assign UUIDs using AutoIDRecord
- Save and load models using BaseManager
- Access fields via both dot and dictionary-style notation
- Update and re-save data
- Read JSON metadata header
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

from WrapDataclass.core.base import BaseModel
from WrapDataclass.manager.base_manager import BaseManager
from WrapDataclass.manager.base_record import AutoIDRecord

# === Configure Logging ===
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

# === Step 1: Define Domain Models ===

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
class Article(AutoIDRecord):  # Auto ID support + manager ready
    title: str
    body: str
    metadata: Metadata

# === Step 2: Initialize a Manager ===

articles_dir = Path("data/articles")
article_manager = BaseManager(Article, articles_dir)

# === Step 3: Create and Save a Record ===

article = Article(
    title="Using WrapDataclass in Production",
    body="This article demonstrates how to serialize dataclasses using WrapDataclass.",
    metadata=Metadata(
        author="Jane Doe",
        created="2025-05-01",
        tags=[Tag(label="dataclass"), Tag(label="serialization", importance=2)]
    )
)

article_manager.save(article, app_name="WrapGuide", version="1.0")

# === Step 4: Load and Use the Record ===

loaded = article_manager.load(article.id)
print("\n[Loaded Article]")
print("ID:", loaded.id)
print("Title:", loaded.title)
print("Author:", loaded.metadata.author)
print("Tags:", [t.label for t in loaded.metadata.tags])

# === Step 5: Iterate & Modify ===
print("\n[All Fields]")
for k, v in loaded.items():
    print(f"{k}: {v}")

loaded["title"] = "Updated: Using WrapDataclass"
print("\n[Updated Title]", loaded.title)

# === Step 6: Save Updated Version ===
article_manager.save(loaded)

# === Step 7: JSON Header Inspection ===
reloaded, header = Article.from_json_with_header(articles_dir / f"{loaded.id}.json")
print("\n[Header Info]")
print("App:", header["app_name"])
print("Version:", header["data_version"])

# === Summary ===
print("\n✅ End-to-end example complete.")
