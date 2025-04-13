import logging
from dataclasses import dataclass
from pathlib import Path
from WrapDataclass.manager.base_manager import BaseManager
from WrapDataclass.manager.base_record import BaseRecord, AutoIDRecord, FlexibleRecord

# === Configure Logging ===
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

# === Models ===

@dataclass
class Note(BaseRecord):
    title: str
    body: str

@dataclass
class NoteGen(AutoIDRecord):
    title: str
    body: str

# === Manual and Auto ID Examples ===

notes_dir = Path("data/notes")
manager_note = BaseManager(Note, notes_dir)
manager_note_gen = BaseManager(NoteGen, notes_dir)

note = Note(id="abc123", title="Manual Note", body="Saved with a manual ID.")
note_gen = NoteGen(title="Generated Note", body="Saved with an auto-generated UUID.")

manager_note.save(note, app_name="NoteApp", version="1.0")
manager_note_gen.save(note_gen, app_name="NoteApp", version="1.0")

loaded_note = manager_note.load(note.id)
loaded_note_gen = manager_note_gen.load(note_gen.id)

print("\n[Manual ID Note]")
print(f"ID: {loaded_note.id}")
print(f"Title: {loaded_note.title}")
print(f"Body: {loaded_note.body}")

print("\n[Auto ID Note]")
print(f"ID: {loaded_note_gen.id}")
print(f"Title: {loaded_note_gen.title}")
print(f"Body: {loaded_note_gen.body}")

# === Flexible ID Example (Optional ID) ===

records_dir = Path("data/flex")
manager_flex = BaseManager(FlexibleRecord, records_dir)

record_manual = FlexibleRecord(id="manual-001", title="Flexible Manual", body="Manual ID provided.")
record_auto = FlexibleRecord(title="Flexible Auto", body="Auto ID assigned.")

manager_flex.save(record_manual, app_name="FlexApp", version="1.0")
manager_flex.save(record_auto, app_name="FlexApp", version="1.0")

loaded_flex_manual = manager_flex.load(record_manual.id)
loaded_flex_auto = manager_flex.load(record_auto.id)

print("\n[Flexible Record - Manual ID]")
print(f"ID: {loaded_flex_manual.id}")
print(f"Title: {loaded_flex_manual.title}")
print(f"Body: {loaded_flex_manual.body}")

print("\n[Flexible Record - Auto ID]")
print(f"ID: {loaded_flex_auto.id}")
print(f"Title: {loaded_flex_auto.title}")
print(f"Body: {loaded_flex_auto.body}")
