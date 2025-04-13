# example_combined.py

from dataclasses import dataclass
from pathlib import Path
from WrapDataclass.core.base import BaseModel
from WrapDataclass.manager.base_manager import BaseManager
from WrapDataclass.manager.base_record import BaseRecord
import logging

# === Configure Logging ===
logging.basicConfig(level=logging.INFO)

# === Models ===

@dataclass
class Summary(BaseModel):
    highlights: list[str]
    conclusion: str

@dataclass
class Evaluation(BaseModel):
    score: float
    notes: str

@dataclass
class DocumentWithSections(BaseRecord):  # Has an ID for manager
    summary: Summary
    evaluation: Evaluation

# === Setup Manager ===

docs_dir = Path("data/documents")
manager = BaseManager(DocumentWithSections, docs_dir)

# === Create Document ===

doc = DocumentWithSections(
    id="doc-001",
    summary=Summary(
        highlights=["Modular", "Typed", "Easy to extend"],
        conclusion="Ready for production use"
    ),
    evaluation=Evaluation(
        score=9.7,
        notes="Well-designed, with clear structure and modularity."
    )
)

# === Save and Load via Manager ===

manager.save(doc, app_name="WrapApp", version="1.0")

loaded_doc = manager.load("doc-001")
print("\n[DocumentWithSections Loaded]")
print("Highlights:", loaded_doc.summary.highlights)
print("Evaluation Score:", loaded_doc.evaluation.score)
