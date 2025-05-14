# WrapDataclass

**WrapDataclass** is a lightweight, modular Python library for working with dataclasses that supports:

- ✅ Nested serialization and deserialization  
- ✅ Optional field skipping  
- ✅ Dict-like access to attributes  
- ✅ JSON read/write with metadata headers  
- ✅ Minimal dependencies (only Python standard library)

This is part of the [WrapTools](https://github.com/WrapTools) ecosystem of composable utilities, designed to be imported individually and only when needed.

---

## 🧩 Key Features

| Feature                  | Description                                               |
|--------------------------|-----------------------------------------------------------|
| `DictMixin`              | Convert dataclasses to/from dictionaries                  |
| `FileMixin`              | Save/load with header metadata (app/version/type)         |
| `DictLikeMixin`          | Use dataclasses like dictionaries (`obj['field']`)        |
| `BaseModel`              | Combines all core mixins for typical use                  |
| `BaseRecord`             | Dataclass with explicit ID for external control           |
| `AutoIDRecord`           | Automatically assigns UUIDs for persistence               |
| `BaseManager`            | Saves and loads records to/from directory as JSON         |
| `from_json_with_header()`| Load both data and metadata (app name, data version, etc.)|

---

## 🚀 Installation

```bash
# Recommended
git clone https://github.com/WrapTools/WrapDataclass
````

---

## 📦 Structure

```
WrapDataclass/
├── core/
│   ├── base.py               # BaseModel combining all mixins
│   ├── mixin_dict.py         # Dict serialization logic
│   ├── mixin_dictlike.py     # Dict-style field access
│   ├── mixin_file.py         # File-based JSON I/O
│   ├── helpers.py            # Dataclass type utilities
│   └── types.py              # TypeVar for reuse
├── manager/
│   ├── base_record.py        # BaseRecord, AutoIDRecord, FlexibleRecord
│   └── base_manager.py       # File manager for persistent models
```

---

## ✍️ Example: Basic Usage

```python
from dataclasses import dataclass
from WrapDataclass.core.base import BaseModel

@dataclass
class Note(BaseModel):
    title: str
    body: str

note = Note(title="Hello", body="World")
note.to_json("note.json", app_name="DemoApp", data_version="1.0")

loaded = Note.from_json("note.json")
print(loaded.title)        # Hello
print(loaded["body"])      # World
```

---

## 🗂️ Example: Managing Records with UUIDs

```python
from dataclasses import dataclass
from WrapDataclass.manager.base_record import AutoIDRecord
from WrapDataclass.manager.base_manager import BaseManager

@dataclass
class Article(AutoIDRecord):
    title: str
    body: str

manager = BaseManager(Article, "data/articles")
article = Article(title="First", body="Example")

manager.save(article)
loaded = manager.load(article.id)
print(loaded.title)
```

---

## 📚 Example Files

| File                 | Purpose                                                   |
| -------------------- | --------------------------------------------------------- |
| `cradle_to_grave.py` | ✅ End-to-end usage demo — models, manager, metadata       |
| `example.py`         | Covers dict-style access, JSON I/O, nested fields         |
| `example_manager.py` | Manual, auto, and flexible ID examples with `BaseManager` |

---

## 🧠 Tips

* Use `BaseModel` when you just need structured data + save/load
* Use `AutoIDRecord` or `BaseRecord` when you want stable IDs with a `BaseManager`
* Use `from_json_with_header()` to inspect `app_name` or `data_version` when loading

---

## ✅ Requirements

* Python 3.10+
* No external dependencies

---

## 🔓 License

MIT License – Free for personal or commercial use.

---

## 🌐 Part of WrapTools

WrapDataclass is part of the [WrapTools GitHub organization](https://github.com/WrapTools), a set of clean, composable Python utilities for real-world development.
